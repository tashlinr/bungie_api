import requests
import json

class Profile:
  """
  A class to find the Total Hours played by a player on Destiny 2.
  Parameters:
  argument1 (str): gamertag of player.

  Returns: 
  # of Total hours played including time logged in.

  """

  header = {"X-API-Key":[YOUR_API_KEY]} #Replace YOUR_API_KEY with your own.
  bungie_html = "https://www.bungie.net/"
  platform = "Platform/"

  def __init__(self, player_name):
    self.player_name = player_name
    self.membershipId = 0
    self.membershipType = ''
    self.characterIds = []

  def get_membership_info(self):
    """ Get membershipID, MembershipType from gamertag/psnid used in search """

    #Endpoint
    #https://www.bungie.net/Platform/Destiny2/SearchDestinyPlayer/{membershipType}/{displayName}/
    search_url = self.bungie_html + self.platform + "Destiny2/SearchDestinyPlayer/-1/"
    search_player = search_url + self.player_name + '/'

    # get request with header api key
    response = requests.get(search_player, headers=self.header)
    #decode json
    my_json = response.content.decode('utf8')
    #load into user friendly version
    data = json.loads(my_json)
    self.membershipId = data['Response'][0]['membershipId']
    self.membershipType = str(data['Response'][0]['membershipType'])
    #print(data)

  def get_character_ids(self):
    """ Get Character IDs from using membership info """
    self.get_membership_info()
    search_character = self.bungie_html + self.platform + "Destiny2/" + \
                       self.membershipType + "/Profile/" + self.membershipId + \
                       "?components=Profiles"
    response = requests.get(search_character, headers=self.header)
    my_json = response.content.decode('utf8')
    data = json.loads(my_json)
    self.characterIds = data['Response']['profile']['data']['characterIds']
    #print(data)

    
  def total_time(self):
    """ Get Total Time from Bungie's API in Minutes """
    total_minutes = 0
    self.get_character_ids()
    
    search_character = self.bungie_html + self.platform + "Destiny2/" + self.membershipType + \
    "/Profile/" + self.membershipId + "/?components=200"

    response = requests.get(search_character, headers=self.header)
    my_json = response.content.decode('utf8')
    data = json.loads(my_json)
    for id in self.characterIds:
      minutes_on_char = int(data['Response']['characters']['data'][id]['minutesPlayedTotal'])
      total_minutes += minutes_on_char    
    return total_minutes

  def print_hours(self):
    """ Print total time in hours """
    print(f'{self.player_name} has {int(self.total_time())/60:.0f} hours total login time!')
