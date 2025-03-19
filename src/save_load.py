class SaveLoad:
    @staticmethod
    def save_game(player):
        if not os.path.exists(SAVE_DIR):
            os.makedirs(SAVE_DIR)
        save_data = {
            "energy": player.energy,
            "money": player.money,
            "inventory": player.inventory.items
        }
        with open(os.path.join(SAVE_DIR, "save1.dat"), "w") as file:
            json.dump(save_data, file)
    
    @staticmethod
    def load_game():
        try:
            with open(os.path.join(SAVE_DIR, "save1.dat"), "r") as file:
                save_data = json.load(file)
                player = Player()
                player.energy = save_data["energy"]
                player.money = save_data["money"]
                player.inventory = Inventory()
                player.inventory.items = save_data["inventory"]
                return player
        except FileNotFoundError:
            return Player()
