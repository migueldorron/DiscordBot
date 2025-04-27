import discord
from discord.ext import commands
import asyncio
import unicodedata


#NORMALIZING MESSAGES
def unicodeReturn(word: str):
    try:
        word_unicode = unicodedata.normalize('NFKD', word.lower())
        word_final = ''.join([char for char in word_unicode if not unicodedata.combining(char)])
        return ' '.join(word_final.split())
    except Exception as e:
        print(f"Error en unicodeReturn: {str(e)}")


#Playing trivia games with questions from a database
class PreguntasTCGPCog(commands.Cog):
    def __init__(self, bot, connectionBBDD):
        self.bot = bot
        self.connectionBBDD = connectionBBDD


    #Adding a question to the database
    @commands.command(name="addquestion", help="For owner use only, if you see this ignore it.")
    async def addquestion(self, ctx, *, args:str):

        #Checking if it's me using the command
        if ctx.author.id != 438078850140864532:
            await ctx.send("You don't own the bot.")
            return

        #If database connection fails        
        if not self.connectionBBDD:
            await ctx.send("Database connection not available.")
            return

        #Formatting checking
        if not args:
            await ctx.send("Please, use the proper format (-addquestion Question, Answer1, Answer 2...).")
            return
        argsList = [arg.strip() for arg in args.split(',') if arg.strip()]
        if len(argsList) < 2:
            print(f"argsList: {argsList}")
            await ctx.send("Please, use the proper format (-addquestion Question, Answer1, Answer 2...).")
            return

        cursor = self.connectionBBDD.cursor()
        try:
            question=True
            idQuestion=None
            for arg in argsList:
                if question:
                
                    cursor.execute("INSERT INTO `preguntas` (`pregunta`) VALUES (%s)", (arg,))
                    question=False
                    idQuestion = cursor.lastrowid

                else:
                    
                    cursor.execute("INSERT INTO `respuestas` (`respuesta`) VALUES (%s)", (arg,))
                    idAnswer = cursor.lastrowid
                    cursor.execute("INSERT INTO `preguntas_respuestas` (`id_pregunta`, `id_respuesta`) VALUES (%s, %s)", (idQuestion, idAnswer))                    
            self.connectionBBDD.commit()
            await ctx.send("Question and answers added successfully.")
        except Exception as e:
            self.connectionBBDD.rollback()
            print(f"Exception: {e}")
        finally:
            cursor.close()

    #Sending a random question to the chat
    @commands.command(name="preguntarandom", help="For owner use only, if you see this ignore it.")
    async def preguntarandom(self, ctx):

        if ctx.author.id != 438078850140864532:
            await ctx.send("You don't own the bot.")
            return        

        if not self.connectionBBDD:
            await ctx.send("Database connection not available.")
            return

        try:
            cursor = self.connectionBBDD.cursor()
            cursor.execute("SELECT preguntas.pregunta FROM preguntas ORDER BY RAND() LIMIT 1")
            random_question = cursor.fetchone()
            if random_question:
                question = random_question[0]
                await ctx.send(question)

            else:
                await ctx.send("No questions in the database.")

        except Exception as e:
            await ctx.send(f"Exception: {e}")

        finally:    
            cursor.close()

    #Main command to play with
    @commands.command(name="trivialtcgp", help="For owner use only, if you see this ignore it.")
    async def trivialtcgp(self, ctx, *, n: int, tiempo=15):

        if ctx.author.id != 438078850140864532:
            await ctx.send("You don't own the bot.")
            return
        
        if not self.connectionBBDD:
            await ctx.send("Database connection not available.")
            return

        if n <= 0:
            await ctx.send("Set a valid number of rounds.")
            return

        playerList = []
        leadingPlayers = []
        try:
            cursor = self.connectionBBDD.cursor()
            await ctx.send(f"¡Trivial a punto de comenzar! Constará de {n} preguntas. Poned los espacios que correspondan y leed MUY bien las preguntas.")
            await asyncio.sleep(2)
            await ctx.send(f"Empezamos en 3...")
            await asyncio.sleep(1)
            await ctx.send(f"Empezamos en 2...")
            await asyncio.sleep(1)
            await ctx.send(f"Empezamos en 1...")
            await asyncio.sleep(1)

            for x in range(n):
                cursor.execute("SELECT * FROM preguntas ORDER BY RAND() LIMIT 1")
                random_question = cursor.fetchone()
                question = random_question[1]
                answerID = random_question[0]
                await ctx.send(f"{x+1}. {question}")

                # Busca las respuestas a esa pregunta en la base de datos
                cursor.execute("""
                    SELECT respuestas.respuesta 
                    FROM respuestas 
                    INNER JOIN preguntas_respuestas 
                    ON preguntas_respuestas.id_respuesta = respuestas.id 
                    WHERE preguntas_respuestas.id_pregunta = %s
                """, (answerID,))
                answers = cursor.fetchall()

                # Normaliza todas las respuestas posibles
                answerList = [unicodeReturn(answer[0]) for answer in answers]
                correct_answer = None

                # Espera a que lleguen mensajes
                while correct_answer is None:
                    try:
                        message = await self.bot.wait_for(
                            "message",
                            timeout=tiempo,
                            check=lambda m: m.channel == ctx.channel
                        )

                        # Toma la ID del usuario y normaliza su mensaje para compararlo con las posibles respuestas
                        ID_usuario = message.author.id
                        answer = message.content
                        user_answer = unicodeReturn(answer)

                        # Respuesta correcta
                        if user_answer in answerList:
                            await ctx.send(f"¡Punto para <@{ID_usuario}>! Una respuesta correcta era '{answerList[0]}'")
                            await asyncio.sleep(2)

                            # Comprobamos si el jugador ya está en la lista
                            player_in_list = next((player for player in playerList if player[0] == ID_usuario), None)

                            if player_in_list:  # Si el jugador ya está, le sumamos un punto
                                player_in_list[1] += 1
                            else:  # Si no está, lo agregamos con 1 punto
                                playerList.append([ID_usuario, 1])

                            # Actualizar la lista de ganadores (los que tienen la puntuación máxima)
                            max_puntos = max([puntos for _, puntos in playerList])  # Encontramos la puntuación máxima
                            leadingPlayers = [str(player[0]) for player in playerList if player[1] == max_puntos]

                            correct_answer = answer

                    # Tiempo agotado
                    except asyncio.TimeoutError:
                        await ctx.send(f"Tiempo agotado. Nadie respondió bien. Una respuesta correcta era '{answerList[0]}'")
                        await asyncio.sleep(2)
                        break  # Salir del bucle en caso de timeout

            # Sistema de puntos final
            if leadingPlayers:
                ganadores = ", ".join([f"<@{id_player}>" for id_player in leadingPlayers])
                await ctx.send(f"¡Felicitaciones a los ganadores! {ganadores}")
            else:
                await ctx.send("No hubo ganadores.")

        finally:
            cursor.close()  # Asegúrate de cerrar el cursor al final

        

async def setup(bot):
    connectionBBDD = bot.connectionBBDD
    await bot.add_cog(PreguntasTCGPCog(bot, connectionBBDD))
