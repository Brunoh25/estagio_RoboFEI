import sys
import rospy
import time
from gsr_ros.srv import StartRequest

sys.path.append('/home/robofei/Workspace/catkin_ws/src/hera_robot/hera_tasks/tasks/methods')

import General as General
import Speech as Speech
import Perception as Perception
import Navigation as Navigation
import Manipulator as Manipulator

# Constant definitions

class SticklerRules:
    count = 0

    def __init__(self):
        rospy.init_node('Stickler for the rules task')
        self.locals = ['room', 'kitche', 'ofice', 'bedroom']

        self.general = General.General()
        self.perception = Perception.Perception()
        self.navigation = Navigation.Navigation()
        self.manipulator = Manipulator.Manipulator()
        self.speech = Speech.Speech()

        self.srv_names = StartRequest()
        # insert forbidden room name:
        self.forbidden_room = 'bedroom'

    def check_person(self):
        name = 'person_' + str(self.count)
        closest_person = self.perception.find_closest_object()
        print(closest_person)
        if closest_person is not None:
            self.count += 1
            self.perception.save_obj_location(name=name, obj=closest_person[0], dist=1)
            return name
        return False
    
    def shoe_rule_speech(self):
        self.speech.speak("I see that you are breaking the shoe rule. Everybody inside the house should not be wearing shoes.")
        self.speech.speak("I'll need you to follow me to the entrance of the house so you can take off your shoes.")

    def forbidden_room_speech(self):
        self.speech.speak("I see that you are breaking the forbidden room rule. You are not allowed to enter this room.")
        self.speech.speak("I kindly request that you leave the bedroom.")
    
    def interact_with_person(self, room):
        breaking_forbidden_room = False
        breaking_shoe_rule = False
        self.speech.speak("Hello, I am Hera, I am here to check if you are following the rules")

        is_wearing_shoes = self.perception.check_shoes()
        if is_wearing_shoes:
            self.shoe_rule_speech()
            self.breaking_shoe_rule = True

        if room == self.forbidden_room:
            self.forbidden_room_speech()
            self.breaking_forbidden_room = True

        return breaking_forbidden_room, breaking_shoe_rule

    def run(self):
        self.speech.say("Starting Stickler for the Rules task")
        # Onde comecar
        self.manipulator.send_goal('way_down')
        # Check forbidden room
        for room in self.locals:

            #self.navigation.goto(room)
            for i in range(2):

                tf_name = self.check_person()
                if tf_name:
                    self.navigation.goto(tf_name)
                    breaking_forbidden_rule, breaking_shoe_rule = self.interact_with_person(room)

                    if breaking_forbidden_rule and room == self.forbidden_room:
                        if i == 0:
                            self.speech.speak("Please, leave this room.")
                        else:
                            self.speech.speak("I see that you might not have understood me. I need you to leave this room, please.")
                    elif not breaking_forbidden_rule and room == self.forbidden_room:
                        self.speech.speak("Nobody is in the forbidden room.")
                    
                    if breaking_shoe_rule:
                        self.speech.speak("Please, follow me.")
                        self.navigation.goto('door')
                        self.speech.speak("Please, take off your shoes.")
                        rospy.sleep(7)
                        self.navigation.goto(room)

        self.speech.speak("I have finished checking the rules. Thank you for your cooperation.")

if __name__ == '__main__':
    try:
        stickler4therules = SticklerRules()
        stickler4therules.run()
    except rospy.ROSInterruptException:
        pass