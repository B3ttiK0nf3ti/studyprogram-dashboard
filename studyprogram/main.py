from setup_controller import SetupController

def main():
    # Create the CLIController via the setup (factory) controller
    controller = SetupController().create_controller()

    # Start the user input loop (CLI interaction)
    controller.handle_user_input()

# Entry point for the script
if __name__ == "__main__":
    main()