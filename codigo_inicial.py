#!/usr/bin/env python3


import rospy
import sys
import time
import rospkg
from hera_speech.srv import imageCaption


path = rospkg.RosPack().get_path('tasks')
sys.path.append(path + '/tasks/methods')


import Navigation, Perception, Manipulator


rooms=0 #números de quartos
sala_proib=1 #situação da sala(0=vazia/1=cheia)
lixo=1 #se possui lixo(0=não/1=sim)


class SticklerForTheRules:
   def __init__(self):
       rospy.init_node('Stickler for the Rules Task')


       self.navigation = Navigation.Navigation()
       self.perception = Perception.Perception()
       self.manipulator = Manipulator.Manipulator()


       self.locals = ['start','person','entrance','garbage','look_garbage','shoes','look_shoes','kitchen','bar']
       self.arena_locals=['entrance','forbidden room','room1']
  
   #NAV/MAP FUNCTIONS
  
   def save_obj(self,i):
       if self.perception.save_obj_location(self.locals[i]):
           if i==1:
               print("Saved person location!")
           elif i==3:
               print("Saved garbage location!")
       time.sleep(4)
       return True
  
   def closest_to_garbage(self):
       obj_name, obj_coordinates=self.perception.find_closest_object('garbage')
       return obj_name, obj_coordinates


   #MANIP FUNCTIONS


   def point_to_object(self,i):
       self.manipulator.send_goal(self.locals[i])
  
   def stop_point(self):
       self.manipulator.send_goal('home')
  
   #UTILS FUNCTIONS


   def search_for_broken_rules(self):
       self.imageCaption("You are seeing an image of a party; you are the supervisor of this party and need to make sure that all three rules are being followed. The first rule is that no one can keep their shoes inside the house; the second is that every party guest needs to be holding a drink; and the third and last one is that there is no garbage on the floor. If you see anyone with their shoes on, you must respond by saying that the first rule was broken, which of the guests is breaking the rule by saying his ID, and if there is another rule that has been broken. If you see anyone without a drink, you must respond by saying that the second rule was broken, which of the guests is breaking the rule by saying his ID, and if there is another rule that has been broken. If you see any garbage on the floor, you must respond by saying that the third rule was broken, which of the guests is the closest to the garbage by saying his ID, and if there is another rule that has been broken. Your answer must follow the format given (first or second or third, ID number, yes or no.")
  
   def person_with_drink(self):
       self.imageCaption("Is the person in the picture holding any type of drink? Answer with yes or no. Your answer can't be anything different from yes or no.")
  
   def person_with_shoes(self):
       self.imageCaption("Is the person in the picture wearing shoes? Answer with yes or no. Your answer can't be anything different from yes or no.")


   def captionGpt(self, context):
       rospy.wait_for_service('imageCaption')
       try:
           caption_image = rospy.ServiceProxy('imageCaption', imageCaption)
           result = caption_image(context)
           print("Received response: " + result.response)
           return result.response
       except rospy.ServiceException as e:
           print("Service call failed: %s"%e)


   def imageCaption (self, context):
       if context is not None:
           context = context
       else:
           context = self.defaultCaptionContext


       try:
           result = self.captionGpt(context)
           self.talk(result)
       except:
           print("Image caption failed")


   #MAIN
  
   def initialize_task(self):
       self.speech.speak('Starting Stickler for the Rules task')
       self.navigation.goto(self.arena_locals[1]) # ir para a sala proibida
       self.manipulator.send_goal('head_down') #olhar para baixo
       while sala_proib==1: #enquanto a sala não estiver vazia
           objects,types = self.perception.find_all_objects() #localizar todos os objetos
           for i in range(len(objects)): #testes para todos os objetos
               if types[i]=="person": #busca por pessoas
                   self.save_obj(1) #salvar localização da pessoa
                   self.point_to_object(1) #apontar para pessoa
                   self.speech.speak('Hi, sorry for disturbing you, but no guests are allowed in this room, please follow me to the other room.')
                   self.stop_point() #parar de apontar
                   break
               elif i==len(objects): #testou todos os objetos e não encontrou pessoa
                   sala_proib=0 #sala vazia
       self.navigation.goto(self.arena_locals[2]) # ir para a primeira sala
       for i in range(2,len(self.arena.locals)): #testes para todas as salas
           objects,types = self.perception.find_all_objects() #localizar todos os objetos
           for j in range(len(objects)): #testes para todos os objetos
               if types[j]=="person": #busca por pessoas
                   if self.person_with_shoes=="yes": #verifica se a pessoa está com sapatos
                       self.save_obj(1)#salvar localização da pessoa
                       self.point_to_object(1) #apontar para pessoa
                       self.speech.speak('Hi, sorry for disturbing you, but all guests have to take off their shoes at the entrance, please follow me i will take you to the entrance.')
                       self.stop_point() #parar de apontar
                       self.navigation.goto(self.arena_locals[0]) #ir para a entrada
                       self.speech.speak('Please take off your shoes and leave them here.')
                       while self.person_with_shoes=="yes": #enquanto a pessoa ainda estiver com sapatos
                           self.speech.speak('Please take off your shoes and leave them here.')
                           time.sleep(10)
                       self.speech.speak('Thank you, you can now go back and enjoy the party.')
                       self.navigation.goto(self.arena_locals[i]) #voltar para a sala onde foi localizado o problema
                   elif self.person_with_drink=="no":#verifica se a pessoa está com uma bebida
                       self.save_obj(1)#salvar localização da pessoa
                       self.point_to_object(1) #apontar para pessoa
                       self.speech.speak('Hi, sorry for disturbing you, but looks you have nothing to drink, please follow me to the kitchen to grab something.')
                       self.stop_point() #parar de apontar
                       self.navigation.goto(self.locals[7]) #ir para a cozinha
                       self.point_to_object(8) #apontar para o bar
                       self.speech.speak('Feel free to take any drink that you like from the bar.')
                       while self.person_with_drink=="no": #enquanto a pessoa não possuir bebida
                           self.speech.speak('Please take any drink that you like from the bar.')
                           time.sleep(10)
                       self.stop_point() #parar de apontar
                       self.speech.speak('Thanks, you can now go back to the party.')
                       self.navigation.goto(self.arena_locals[i]) #voltar para a sala onde foi localizado o problema
               elif types[j]=="garbage": #busca por lixo
                   self.save_obj(3) #salvar localização do lixo
                   obj_name,obj_cord=self.closest_to_garbage() #localiza pessoa mais próxima do lixo
                   self.manipulator.send_goal(obj_cord) #aponta para pessoa mais próxima do lixo
                   self.speech.speak('Hi, sorry for disturbing you, but littering is not allowed in this house, can you please take the garbage from the floor and  throw it into the bin.')
                   while lixo==1: #enquanto localizar lixo
                       objects,types = self.perception.find_all_objects() #localizar todos os objetos
                       for k in range(len(objects)): #testes para todos os objetos
                           if types[k]=="garbage": #verifica se há lixo
                               self.speech.speak('Please take the garbage from the floor and  throw it into the bin.')
                               time.sleep(10)
                               break
                           elif k==len(objects): #testou todos objetos e não há lixo
                               lixo=0 #sem lixo
                   self.stop_point() #parar de apontar
                   self.speech.speak('Thank you for the help, I really appreciate.')
               self.navigation.goto(self.arena_locals[i+1]) #ir para próxima sala


if __name__ == "__main__":
   task = SticklerForTheRules()
   task.initialize_task()
