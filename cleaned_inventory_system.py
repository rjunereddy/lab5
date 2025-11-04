"""
Inventory Management System
A secure and robust system for managing inventory with proper error handling.
"""

import json
import logging
from datetime import datetime
from typing import Dict, List, Optional

# Initialize logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Global variable for stock data
stock_data: Dict[str, int] = {}


def add_item(item: str = "default", quantity: int = 0, logs: Optional[List[str]] = None) -> None:
    """
    Add an item to the inventory.
    
    Args:
        item: Name of the item to add
        quantity: Quantity to add (positive number)
        logs: Optional list to log operations
    """
    if logs is None:
        logs = []
    
    # Input validation - this fixes the TypeError you encountered
    if not item or not isinstance(item, str):
        logging.warning("Invalid item name: %s. Item must be a non-empty string.", item)
        return
    
    if not isinstance(quantity, int):
        logging.warning("Invalid quantity type: %s. Quantity must be an integer.", type(quantity).__name__)
        return
    
    if quantity < 0:
        logging.warning("Invalid quantity: %d. Quantity cannot be negative.", quantity)
        return
    
    stock_data[item] = stock_data.get(item, 0) + quantity
    log_message = f"{datetime.now()}: Added {quantity} of {item}"
    logs.append(log_message)
    logging.info(log_message)


def remove_item(item: str, quantity: int) -> bool:
    """
    Remove an item from inventory.
    
    Args:
        item: Name of the item to remove
        quantity: Quantity to remove
        
    Returns:
        bool: True if successful, False otherwise
    """
    if item not in stock_data:
        logging.warning("Item not found: %s", item)
        return False
    
    if not isinstance(quantity, int) or quantity <= 0:
        logging.warning("Invalid quantity for removal: %s", quantity)
        return False
    
    try:
        stock_data[item] -= quantity
        if stock_data[item] <= 0:
            del stock_data[item]
            logging.info("Removed item %s completely", item)
        else:
            logging.info("Removed %d of %s", quantity, item)
        return True
    except (KeyError, ValueError) as error:
        logging.error("Error removing item %s: %s", item, error)
        return False


def get_quantity(item: str) -> Optional[int]:
    """
    Get quantity of an item.
    
    Args:
        item: Name of the item
        
    Returns:
        Optional[int]: Quantity if item exists, None otherwise
    """
    if item not in stock_data:
        logging.warning("Item not found: %s", item)
        return None
    return stock_data[item]


def load_data(filename: str = "inventory.json") -> bool:
    """
    Load inventory data from JSON file.
    
    Args:
        filename: Name of the file to load from
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            global stock_data
            loaded_data = json.load(file)
            # Validate loaded data structure
            if isinstance(loaded_data, dict):
                stock_data = loaded_data
                logging.info("Data loaded successfully from %s", filename)
                return True
            else:
                logging.error("Invalid data format in %s", filename)
                return False
    except (FileNotFoundError, json.JSONDecodeError, IOError) as error:
        logging.error("Error loading data from %s: %s", filename, error)
        return False


def save_data(filename: str = "inventory.json") -> bool:
    """
    Save inventory data to JSON file.
    
    Args:
        filename: Name of the file to save to
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(stock_data, file, indent=4)
        logging.info("Data saved successfully to %s", filename)
        return True
    except IOError as error:
        logging.error("Error saving data to %s: %s", filename, error)
        return False


def print_data() -> None:
    """Print all inventory data."""
    if not stock_data:
        print("No items in inventory.")
        return
    
    print("Inventory Report:")
    print("-" * 20)
    for item_name, quantity in stock_data.items():
        print(f"{item_name} -> {quantity}")
    print("-" * 20)


def check_low_items(threshold: int = 5) -> List[str]:
    """
    Check for items with low stock.
    
    Args:
        threshold: Minimum quantity threshold
        
    Returns:
        List[str]: List of items below threshold
    """
    low_items = []
    for item_name, quantity in stock_data.items():
        if quantity < threshold:
            low_items.append(item_name)
    return low_items


def main() -> None:
    """Main function to demonstrate inventory system."""
    # Test the inventory system with proper data
    add_item("apple", 10)
    add_item("banana", 5)
    
    # These should now be handled properly with warnings
    add_item("", 10)  # Invalid item name
    add_item("orange", -2)  # Invalid quantity
    add_item(123, 10)  # Wrong type for item name - THIS WOULD CRASH IN ORIGINAL
    
    remove_item("apple", 3)
    remove_item("orange", 1)  # Item doesn't exist
    
    apple_quantity = get_quantity("apple")
    print(f"Apple stock: {apple_quantity}")
    
    low_items = check_low_items(threshold=5)
    print(f"Low items: {low_items}")
    
    save_data()
    load_data()
    print_data()
    
    # Safe alternative to eval
    print("Safe print without eval")


if __name__ == "__main__":
    main()