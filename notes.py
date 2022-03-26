import datetime
import argparse
import os

# arg parsing
parser = argparse.ArgumentParser(description="Create and organize programming notes.")

# python notes.py -n "note text goes here"
parser.add_argument(
    "-n",
    help="Add a new note.",
    nargs="?",
    const="-- note text goes here --",
)

parser.add_argument(
    "-t",
    nargs="+",
    help="Add tags to a note during creation.",
)

parser.add_argument(
    "-o",
    action="store_const",
    const=True,
    help="Open note in VS Code after creation.",
)

parser.add_argument(
    "-s",
    action="store_const",
    const=True,
    help="Enter note search tool.",
)

parser.add_argument(
    "-d",
    nargs="+",
    help="Add organization levels, e.g., 'projectname projecttopic' becomes 'notes.projectname.projecttopic'.",
)

# parse arguments
args = parser.parse_args()

# time stamp
cur_datetime = datetime.datetime.now()

str_datetime = cur_datetime.strftime("%Y%m%d%H%M%S")

# notes directory
dir_name = "notes"

if not os.path.exists(dir_name):
    os.makedirs(dir_name)

# new note actions
if args.n:

    with open(dir_name + "/" + str_datetime + ".txt", "w") as file:

        file.write("timestamp: " + cur_datetime.strftime("%Y-%m-%d %H:%M:%S.%f"))

        file.write("\n")
        file.write("organization: ")
        if args.d:
            file.write(".".join(args.d))
        else:
            file.write("None")

        file.write("\n")
        file.write("tags: ")
        if args.t:
            file.write(",".join(args.t))
        else:
            file.write("None")

        file.write("\n########## DON'T EDIT ABOVE ##########\n")

        file.write("\n")
        file.write(args.n)

    # open in vs code
    if args.o:
        os.system("code " + dir_name + "/" + str_datetime + ".txt")

    # update index
    note_list = []

    notes = os.listdir(dir_name)
    for note in notes:
        if os.path.isfile(os.path.join(dir_name, note)):
            with open(os.path.join(dir_name, note), "r") as file:

                # date
                date_text = file.readline()
                date_text = date_text.replace("timestamp: ", "")
                date_text = date_text.replace("\n", "")
                date_time = datetime.datetime.strptime(
                    date_text, "%Y-%m-%d %H:%M:%S.%f"
                )

                # organization
                org_text = file.readline()
                org_list = None
                org_text = org_text.replace("organization: ", "")
                org_text = org_text.replace("\n", "")
                org_list = org_text.split(sep=",")

                # tags
                tag_text = file.readline()
                tag_list = None
                tag_text = tag_text.replace("tags: ", "")
                tag_text = tag_text.replace("\n", "")
                tag_list = tag_text.split(sep=",")

            note_list.append(
                {"date": date_time, "organization": org_list, "tags": tag_list}
            )

    # # file to store metadata
    with open(".notes", "w") as file:

        for note in note_list:

            file.write(note["date"].strftime("%Y%m%d%H%M%S"))

            if note["organization"]:
                file.write(" ")
                file.write(",".join(note["organization"]))

            if note["tags"]:
                file.write(" ")
                file.write(",".join(note["tags"]))

            file.write("\n")
