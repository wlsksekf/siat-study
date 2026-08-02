class Team:
    def __init__(self):
        self.members = []

    def add_member(self, name):
        self.members.append(name)

    def __iter__(self):
        return iter(self.members)
        
my_team = Team()
my_team.add_member("Alice")
my_team.add_member("Bob")

for member in my_team:
    print(member)

for member in my_team:
    print(member)