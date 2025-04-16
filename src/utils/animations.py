import asyncio
import sys
import os
from telethon.errors.rpcerrorlist import FloodWaitError

# Add parent directory to path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

# ref : https://emojicombos.com/cat-text-art

# Animation frames for thinking message - Hand animation
THINKING_ANIMATIONS = [
    "⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣤⣤⣄⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⠀⠀⣴⣿⠟⠛⠛⠛⠿⣿⣿⣿⣿⣶⣤⡀⠀⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⣠⣴⣿⡟⠁⢀⣤⣀⠀⠀⠀⠀⠀⠀⠉⠻⣿⣦⠀⠀⠀⠀\n⠀⠀⠀⠀⣾⡿⠿⠛⠁⣰⣿⣿⣿⡆⠀⠀⣴⣶⣶⠄⠀⢻⣿⡄⠀⠀⠀\n⠀⠀⣾⡿⠁⠀⠀⠀⠀⠻⣿⣿⣿⠃⠀⣼⣿⣿⣿⠀⠀⠀⢿⣷⣄⠀⠀\n⠀⣾⣿⠁⠀⣤⣶⡄⠀⠀⠈⠉⠁⠀⠀⠈⠛⠊⠁⠀⠀⠀⠀⠙⢿⣷⠀\n⠀⣿⡇⠀⢸⣿⣿⡿⡆⠀⠀⣴⣶⣶⣴⣶⣄⠀⠀⢠⣶⣿⣦⠀⠀⣿⡇\n⠀⣿⡇⠀⠀⠛⠙⠉⠀⣰⣿⣿⣿⣿⣿⣿⣿⣇⠀⣿⣿⣿⣿⠀⠀⣿⡇\n⠀⣿⣇⠀⠀⠀⠀⢀⣾⣿⣿⣿⣿⣿⣿⣷⣿⣷⡀⠀⠉⠉⠀⠀⣸⣿⠇\n⠀⣿⣿⠀⠀⠀⠀⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⣻⡟⠘\n⠀⢹⣿⠀⠀⠀⠀⠀⠉⠛⠉⠁⠉⠁⠙⠻⠿⠟⠀⠀⠀⠀⠀⣾⣿⠁⠀\n⠀⠀⣿⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⡏⠀⠀\n⠀⠀⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⡇⠀⠀\n⠀⠀⣻⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⡇⠀⠀\n⠀⠀⢸⣿⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⡇⠀⠀",
    "⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣤⣤⣄⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⠀⠀⣴⣿⠟⠛⠛⠛⠿⣿⣿⣿⣿⣶⣤⡀⠀⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⣠⣴⣿⡟⠁⢀⣤⣀⠀⠀⠀⠀⠀⠀⠉⠻⣿⣦⠀⠀⠀⠀\n⠀⠀⠀⠀⣾⡿⠿⠛⠁⣰⣿⣿⣿⡆⠀⠀⣴⣶⣶⠄⠀⢻⣿⡄⠀⠀⠀\n⠀⠀⣾⡿⠁⠀⠀⠀⠀⠻⣿⣿⣿⠃⠀⣼⣿⣿⣿⠀⠀⠀⢿⣷⣄⠀⠀\n⠀⣾⣿⠁⠀⣤⣶⡄⠀⠀⠈⠉⠁⠀⠀⠈⠛⠊⠁⠀⠀⠀⠀⠙⢿⣷⠀\n⠀⣿⡇⠀⢸⣿⣿⡿⡆⠀⠀⣴⣶⣶⣴⣶⣄⠀⠀⢠⣶⣿⣦⠀⠀⣿⡇\n⠀⣿⡏⠀⠀⠛⠙⠉⠀⣰⣿⣿⣿⣿⣿⣿⣿⣇⠀⣿⣿⣿⣿⠀⠀⣿⡇\n⠀⣿⣧⠀⠀⠀⠀⢀⣾⣿⣿⣿⣿⣿⣿⣷⣿⣷⡀⠀⠉⠉⠀⠀⣸⣿⠃\n⠀⣿⣿⠀⠀⠀⠀⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⣿⡏⠀\n⠀⢹⣿⠀⠀⠀⠀⠀⠉⠛⠉⠁⠉⠁⠙⠻⠿⠟⠀⠀⠀⠀⠀⣼⣿⠀⠀\n⠀⠀⣿⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⠀⠀\n⠀⠀⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⠀⠀\n⠀⠀⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⡿⠀⠀\n⠀⠀⢿⣿⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣿⣿⠃⠀⠀",
    "⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣤⣤⣄⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⠀⠀⣴⣿⠟⠛⠛⠛⠿⣿⣿⣿⣿⣶⣤⡀⠀⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⣠⣴⣿⡟⠁⢀⣤⣀⠀⠀⠀⠀⠀⠀⠉⠻⣿⣦⠀⠀⠀⠀\n⠀⠀⠀⠀⣾⡿⠿⠛⠁⣰⣿⣿⣿⡆⠀⠀⣴⣶⣶⠄⠀⢻⣿⡄⠀⠀⠀\n⠀⠀⣾⡿⠁⠀⠀⠀⠀⠻⣿⣿⣿⠃⠀⣼⣿⣿⣿⠀⠀⠀⢿⣷⣄⠀⠀\n⠀⣾⣿⠁⠀⣤⣶⡄⠀⠀⠈⠉⠁⠀⠀⠈⠛⠊⠁⠀⠀⠀⠀⠙⢿⣷⠀\n⠀⣿⡇⠀⢰⣿⣿⡇⡆⠀⠀⣴⣶⣶⣴⣶⣄⠀⠀⢠⣶⣿⣦⠀⠀⣿⠇\n⠀⣿⡇⠀⠀⠛⠛⠉⠀⣰⣿⣿⣿⣿⣿⣿⣿⣇⠀⣿⣿⣿⣿⠀⠀⣿⠀\n⠀⣿⣇⠀⠀⠀⠀⢀⣾⣿⣿⣿⣿⣿⣿⣷⣿⣷⡀⠀⠉⠉⠀⠀⣸⣿⠀\n⠀⣿⣿⠀⠀⠀⠀⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⣿⣿⠀\n⠀⠘⣿⡄⠀⠀⠀⠀⠉⠛⠉⠁⠉⠁⠙⠻⠿⠟⠀⠀⠀⠀⠀⣸⣿⠃⠀\n⠀⠀⢿⣷⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣿⡿⠀⠀\n⠀⠀⠘⣿⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣿⡿⠁⠀⠀\n⠀⠀⠀⠈⠻⣦⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⣾⡿⠋⠀⠀⠀⠀"
]

# New text art for initial messages
INITIAL_MESSAGE_ART = """
⠀⠀⠀⠀⠀⣠⣤⣤⣤⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⣤⣤⣄⡀⠀⠀⠀⠀
⠀⠀⠀⢀⣾⡟⠉⠀⠙⠻⣷⣦⡀⠀⠀⠀⠀⠀⣠⣶⠿⠋⠁⠈⠻⣿⡄⠀⠀⠀
⠀⠀⢠⣿⠏⠀⠀⠀⠀⠀⣈⣻⣿⣴⣶⣶⣦⣾⣟⣁⠀⠀⠀⠀⠀⠘⣿⡆⠀⠀
⠀⢀⣾⡏⠀⠀⣠⣴⠾⠟⠋⠉⠁⠀⠀⠀⠀⠈⠉⠙⠻⢳⣦⣄⡀⠀⠸⣿⡄⠀
⠀⢸⡿⢀⣴⠟⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠙⠻⣦⡀⢻⣧⠀
⠀⣿⣷⣿⣅⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢈⣿⣮⣿⡄
⢀⣿⣿⡏⢻⣦⠀⠀⠀⣀⠀⠀⠀⡀⠀⠀⢀⡀⠀⠀⣀⠀⠀⠀⢠⣾⢻⣿⣿⡇
⣸⡿⠸⣡⠀⠹⣧⡀⠀⣿⣷⣠⡾⢻⣦⣴⠟⣷⣤⡾⣿⠀⠀⣰⡿⠁⢸⡿⢻⣧
⣿⠇⠀⠙⠷⠶⠟⠃⠀⣿⠈⠛⠀⠀⠙⠋⠀⠈⠛⠁⣿⠀⠀⠛⠷⠶⠟⠁⠘⣧
⣿⠀⠀⠀⠀⠀⠀⠀⠀⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⠀⠀⠀⠀⠀⠀⠀⠀⣿
⢿⣇⠀⠀⠀⠀⠀⠀⠀⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⠀⠀⠀⠀⠀⠀⠀⢰⣏
⠘⣿⣄⠀⠀⠀⠀⠀⠀⣿⣴⣷⣄⢠⣾⣷⡀⣴⣷⣄⣿⠀⠀⠀⠀⠀⠀⢠⣿⠇
⠀⠘⢿⣦⣀⠀⠀⠀⠀⠿⠋⠀⠙⠟⠁⠈⠻⠏⠀⠙⠿⠀⠀⠀⠀⣀⣴⡿⠋⠀
⠀⠀⠀⠉⠻⢿⣶⣤⣄⣀⣀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣀⣠⣤⣶⡾⠟⠋⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠈⠉⠉⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠋⠉⠁⠀⠀⠀⠀⠀⠀"""


INITIAL_MESSAGE_ART_2 = """ 
⠀⡴⢢⠀⠀⠀⠀⣠⠲⣄⠀⠀⠀⠀⠀⠀
⠀⣇⠀⠓⠒⠒⠲⠇⠀⢘⠀⠀⡏⠙⣆⠀
⡼⠁⣀⡀⠀⠀⣀⡀⠀⠩⡄⠀⢣⠀⠘⡄
⡇⠀⠿⠇⠀⠀⠿⠇⠀⠀⡇⠀⠀⡇⠀⢧
⠹⣄⠀⠤⠛⠤⠄⠀⠀⣠⠅⠀⠀⣾⠀⣸
⠀⠀⠛⣦⠒⠒⠒⠒⠋⠓⠒⠒⠛⠁⣼⠀
⠀⠀⠀⣸⠀⠀⠀⠀⠀⠀⠀⠀⠀⠏⠀⠀
⠀⠀⠀⣾⠀⡄⠀⢶⡴⠤⡄⢠⠀⡇⠀⠀
⠀⠀⠀⣫⣴⣇⣀⣻⠁⠀⢸⣞⣀⣇⠀⠀"""


INITIAL_MESSAGE_ART_3 = """


"""

# Simplified version for cases where we might hit rate limits
SIMPLE_INITIAL_MESSAGE = "Thinking..."

async def animated_thinking(message, task):
    """
    Display an animated hand while waiting for a task to complete.
    
    Args:
        message: The message object to update with animation frames
        task: The asyncio task to wait for
    
    Returns:
        The result of the task
    """
    animation_index = 0
    dots = 1
    
    # Rate limiting variables
    last_edit_time = 0
    min_edit_interval = 1.5  # Start with 1.5 seconds between edits
    consecutive_errors = 0
    max_consecutive_errors = 3
    
    # Continue animation until the task completes
    while not task.done():
        # Create thinking text with animated dots
        thinking_text = "Thinking" + "." * dots + "\n\n"
        
        # Update the message with the current animation frame and thinking text
        current_frame = thinking_text + THINKING_ANIMATIONS[animation_index]
        
        # Check if we need to wait before editing to respect rate limits
        current_time = asyncio.get_event_loop().time()
        time_since_last_edit = current_time - last_edit_time
        
        if time_since_last_edit < min_edit_interval:
            # If not enough time has passed, wait before editing
            await asyncio.sleep(min_edit_interval - time_since_last_edit)
        
        try:
            # Attempt to edit the message
            await message.edit(current_frame)
            last_edit_time = asyncio.get_event_loop().time()
            consecutive_errors = 0  # Reset error counter on success
            
        except FloodWaitError as e:
            consecutive_errors += 1
            wait_seconds = getattr(e, 'seconds', 15)
            
            # Log the error
            print(f"FloodWaitError in animated_thinking: {wait_seconds}s wait required")
            
            # Increase the minimum interval between edits
            min_edit_interval = max(min_edit_interval * 2, wait_seconds / 10)
            print(f"Increasing minimum edit interval to {min_edit_interval}s")
            
            # If we have too many consecutive errors, stop the animation
            if consecutive_errors >= max_consecutive_errors:
                print(f"Too many consecutive FloodWaitErrors ({consecutive_errors}). Stopping animation.")
                break
                
            # Wait a bit before trying again
            await asyncio.sleep(min(10, wait_seconds / 5))
            
        except Exception as e:
            # Log other errors but continue animation
            print(f"Error updating animation: {str(e)}")
            await asyncio.sleep(5)  # Wait longer after generic errors
            
        # Move to the next animation frame
        animation_index = (animation_index + 1) % len(THINKING_ANIMATIONS)
        
        # Update dots (cycle between 1-3 dots)
        dots = dots % 3 + 1
        
        # Wait before next animation frame - adaptive based on errors
        await asyncio.sleep(min_edit_interval / 2)
    
    # Return the result of the completed task
    return await task