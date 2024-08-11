from controller.UserCardsController import UserCardsController

class InventoryManager:
  def __init__(self, conn):
    self.conn = conn
    self.userCardsController = UserCardsController(conn)
    
  def showUserInventory(self, user_id):
    all_cards = self.userCardsController.getCardByUser(user_id)
    print(all_cards)
    return {
      'header': 'show_user_inventory',
    }