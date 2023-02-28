import getopt
import sys

def main(argv):
    # Define the expected positional arguments
    positional_args = 'arg1 arg2 arg3'

    try:
        # Pass the argument list and the expected positional arguments
        opts, args = getopt.getopt(argv, "", [positional_args])
    except getopt.GetoptError:
        # Handle error in case the arguments are not passed correctly
        print("Your command line arguments are incorrect.")
        sys.exit(2)

    # Extract the positional arguments from the list of arguments
    arg1, arg2, arg3 = args

    # Use the positional arguments
    print(f"arg1: {arg1}")
    print(f"arg2: {arg2}")
    print(f"arg3: {arg3}")

if __name__ == "__main__":
    main(sys.argv[1:])