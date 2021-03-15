
import random
import simpy


# Caracteristicas de la computadora
CPU_VELOCITY = 3 # Canridad de intrucciones que el CPU ejecuta por unidad de tiempo
CPU_QUANTITY = 1 # Cantidad de procesadores disponibles
PROCESS = 200 # Cantidad de procesos
INTERVALS = 1
TIME_UNIT = 1 # Tiempo que se tarda en ejecutar 3 intrucciones (Unidad de tiempo)
RAM_QUANTITY = 100 # Tiempo que se tarda en ejecutar 3 intrucciones (Unidad de tiempo)

# Clase que modela el comportamiento de una computadora
class Computer:

    def __init__(self, env):
        super().__init__()
        self.CPU = simpy.Resource(env, capacity=CPU_QUANTITY)
        self.RAM = simpy.Container(env, init=RAM_QUANTITY, capacity=RAM_QUANTITY)   


# Simula un proceso
def process_item(id, env, computer, ram_req, inst_req, initial_time):
    # print(f"[Generado] Proceso {id}, Instrucciones {inst_req}, a las {env.now}")

    # Recorre y verifica sis existe un CPU libre
    with computer.CPU.request() as req:

        yield req

        # Mira si existe suficiente memoria RAM
        if computer.RAM.level >= ram_req:
            
            # Obtiene la memoria necesaria de la computadora
            yield computer.RAM.get(ram_req)
            yield env.timeout(TIME_UNIT)

            # Mira si todavía quedan instrucciones pendientes
            next_inst = inst_req - CPU_VELOCITY
            
            # Si todavía quedan genera otra vez el proceso con las instrucciones restantes
            if  next_inst > 0:
                yield computer.RAM.put(ram_req)

                env.process(process_item(id, env, computer, ram_req, next_inst, initial_time))
            else:
                # Finaliza el proceso
                tiempo = env.now - initial_time
                print(f'[!] Proceso {id} se ejecuto en {tiempo}')
                yield computer.RAM.put(ram_req)

        else:
            # Si no hay suficiente RAM, vuelve a generar el proceso hasta que exista memoria
            env.process(process_item(id, env, computer, ram_req, inst_req, initial_time))



# Genera un nuevo proceso
def process_generator(env, computer):

    # Genera la cantidad de procesos indicada
    for e in range(PROCESS):
        
        # Genera la cantidad de memoria ram e intrucciones requeridas 
        ram_req = random.randint(1, 10)
        inst_req = random.randint(1, 10)
    
        # Genera el proceso
        env.process(process_item(e, env, computer, ram_req, inst_req, env.now))

        yield env.timeout(INTERVALS)

    
def main():

    print(":: SIMULADOR ::\n")

    env = simpy.Environment()
    computer = Computer(env)
    process_gen = env.process(process_generator(env, computer))
    env.run()


if __name__ == '__main__':
    main()
    