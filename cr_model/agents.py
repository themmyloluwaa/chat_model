from mesa import Agent
import random

# women --> 20%
# it's not about constant variables but distributions
# prematch will not happen if filters are applied which may not result in quids deduction??
# several types of agents with different conversation success rate.
# Base behaviour for users e.g. bad for 20 seconds
class CRUser(Agent):
   def __init__(self, unique_id, model, pos, moore, gender, gender_preference, wait_duration=10):
      super().__init__(unique_id, model)
      self.gender = gender
      self.quid = 30
      self.no_of_matches = 0
      self.gender_preference = gender_preference
      self.prematch_quid_amount = 5
      self.wait_duration = wait_duration
      self.pos = pos
      self.moore = moore
      self.is_matched = False

   def check_preference(self,potential_partner_gender):
         return self.gender_preference == potential_partner_gender
   def add_to_quid(self, amount):
      self.quid += amount

   def deduct_from_quid(self, amount):
      self.quid = self.quid - amount if self.quid - amount != 0 else 0

   def prematch(self):
      """
      Prematch algorithm that handles picking a partner and 
      starting a conversation with them if their preferences match.
      """
      my_cell = self.model.grid.get_cell_list_contents([self.pos])
      my_cell = list(filter(lambda x: x.is_matched == False, my_cell))
      if len(my_cell) > 1:
         # set customer to self for while loop condition
         customer = self
         while customer == self:
            """select a random person from the people at my location
            to match with"""
            customer = self.random.choice(my_cell)

         """Deduct suggestion tax from both users"""
         self.deduct_from_quid(self.prematch_quid_amount)
         customer.deduct_from_quid(self.prematch_quid_amount)
         """Check if the preferences match"""
         match_success = self.check_preference(customer.gender) == customer.check_preference(self.gender)
         """If the preferences match or they just would like to have a conversation irrespective of prefrences. 
            Initialize chat and reward users with selection reward.
            Begin the chat and increment count of matches each user has.
            Set match_status to True to ensure we they don't get matched with other users in the same step.
            Move both users to new location.
         """
         if match_success or random.randint(0, 1) == 1:
            chat = CRChat(self.unique_id, self.model, self, customer)
            self.add_to_quid(8)
            customer.add_to_quid(8)
            chat.begin_chat()
            self.no_of_matches += 1
            customer.no_of_matches += 1
            self.is_matched = True
            customer.is_matched = True
            self.move()
            customer.move()

   def wait_for_quid(self):
      """
      If this user is too poor to enter a pool for matching, give them 5 quids.
      """
      self.add_to_quid(5)
      self.move()

   def move(self):
      possible_steps = self.model.grid.get_neighborhood(
         self.pos, moore=self.moore, include_center=False
      )
      new_position = self.random.choice(possible_steps)
      self.model.grid.move_agent(self, new_position)

         
   def step(self) -> None:
      """
      At each step of the agent, If they have not been matched yet and they have enough wealth for entring
      the pool, then try to match. Else If they have not been matched but with insufficient wealth, increase their
      wealth.

      If they have been previously matched, set match status to False so they can be matched in next step. 
      """
      if not self.is_matched:
         if self.quid >= 15:
            self.prematch()
         else:
            self.wait_for_quid()
      else:
         self.is_matched = False


       


class CRChat(Agent):
   def __init__(self, unique_id, model, user_a, user_b,avg_chat_dur=30, max_chat_dur=300):
      super().__init__(unique_id, model)
      self.avg_chat_dur = avg_chat_dur
      self.max_chat_dur = max_chat_dur
      self.user_a = user_a
      self.user_b = user_b
      self.chat_duration = 0
      self.chat_reward_per_two_seconds = 1
      print(user_a.unique_id,"," ,user_b.unique_id,",")

   def calculate_reward(self):
      reward = 0
      if self.chat_duration % 2 == 0:
         reward = ((self.chat_duration // 2) * self.chat_reward_per_two_seconds)
      else:
         reward = ((self.chat_duration // 2) * self.chat_reward_per_two_seconds) + 1
      return reward


   def begin_chat(self):
      self.chat_duration = random.randint(self.avg_chat_dur, self.max_chat_dur)
      reward_amount = self.calculate_reward()
      self.user_a.add_to_quid(reward_amount)
      self.user_b.add_to_quid(reward_amount)
