#!/bin/bash

import authenticate
import upload
import query


class Menu:

    def __init__(self):

        self.__items = {  # menu items stand for all options available
            "1": {"1": ["Authentication", "Sign In"], "2": ["Authentication", "Sign Out"],
                  "3": ["Authentication", "Sign Up"]},
            "2": {"1": "Upload"},
            "3": {"1": ["Query", "Seek Images By A List of Tags"], "2": ["Query", "Seek Images By an Image"],
                  "3": ["Query", "Add Tags to a Cloud Image"], "4": ["Query", "Delete Image By Id"]},
            "4": {"1": "Quit"}
        }

        # id_token is passed in headers["auth":id_token]
        self.__id_token = None

    def __show_program_info(self):
        print("--------------------------------------------------------------")
        print("\n")
        print("\n")
        print("           Monash FIT5225 2021 SM1 - Assignment2")
        print("         TagTag: A Modern Image Storage on the Cloud")
        print("\n")
        print("                     Developers:Group 30")
        print("\n")
        print("\n")
        print("--------------------------------------------------------------")

    def __show_general_menu(self):

        print("---------------------------- Menu ----------------------------")
        print("\n")
        for outer_index, subdict in self.__items.items():

            # a signal for jumpping loop to prevent repeatation
            last_general_menu_item = ""
            for inner_index, menu_item in subdict.items():

                general_menu_item = ""  # a general item like "Authentication", "Upload", etc is chosen as signal.

                # if there is are sub-menus
                if (str(type(menu_item)) == "<class 'list'>"):
                    general_menu_item = menu_item[0]

                # if there is no sub-menu
                if (str(type(menu_item)) == "<class 'str'>"):
                    general_menu_item = menu_item

                if (general_menu_item != last_general_menu_item):
                    print(outer_index + ". " + general_menu_item)
                    last_general_menu_item = general_menu_item

        print("\n")
        print("--------------------------------------------------------------")

    def __show_specific_menu(self, general_menu_id):

        print("-------------------------- Choice {} --------------------------".format(general_menu_id))
        print("\n")
        subdict = self.__items[general_menu_id]

        for inner_index, menu_item in subdict.items():
            print(general_menu_id + "." + inner_index + " " + menu_item[1])

        print("\n")
        print("--------------------------------------------------------------")

    def menu_start(self):

        # a menu loop repeat until user select quit option
        while (True):
            # show project info
            self.__show_program_info()

            # show primary menu
            self.__show_general_menu()

            choice = input("Please enter an option. For example, 1\n")

            # if a user selects authenticate menu
            if (choice == "1"):
                self.__show_specific_menu(choice)
                choice = input("Please enter an option. For example, 1\n")
                # if user choose sign in or sign up
                if (choice == "1" or choice == "3"):
                    self.__id_token = authenticate.log_in()

                # if user choose sign out
                if (choice == "2"):
                    self.__id_token = None

            # if a user selects upload menu
            if (choice == "2"):
                # if user has signed in
                if (self.__id_token != None):
                    print("------------------------ Upload Folder ------------------------")
                    print("\n")

                    image_list = upload.list_images()
                    image_list_length = len(image_list)
                    for i in range(image_list_length):
                        print("\n" + str(i + 1) + ". " + image_list[i])

                    option = int(input("Please enter an option. For example, 1\n"))

                    # valiate option ensure it fall into the range
                    if (option > 0 and option < image_list_length + 1):
                        result = upload.upload_image(image_list[option - 1], self.__id_token)
                        print(result)

                    print("\n")
                    print("--------------------------------------------------------------")
                # if user has not signed in
                else:
                    self.__show_specific_menu("1")
                    print("\nPlease Sign In or Sign Up")
                    choice = input("Please enter an option. For example, 1\n")
                    if (choice == "1" or choice == "3"):
                        self.__id_token = authenticate.log_in()
                    if (choice == "2"):
                        self.__id_token = None

            # if a user selects query menu
            if (choice == "3"):
                # if user has signed in
                if (self.__id_token != None):
                    self.__show_specific_menu(choice)
                    choice = input("Please enter an option. For example, 1\n")

                    # if user choose to seek images by tages
                    if (choice == "1"):
                        tags_str = input("\nplease input tags separated by comma")
                        tags = tags_str.split(",")
                        print("\ntags:" + tags)
                        links = query.seek_images_by_tags(tags, self.__id_token)
                        print("\nlinks:")
                        print(links)

                    # if user choose to seek images by a image
                    if (choice == "2"):
                        print("------------------------ Upload Folder ------------------------")
                        print("\n")

                        image_list = upload.list_images()
                        image_list_length = len(image_list)
                        for i in range(image_list_length):
                            print("\n" + str(i + 1) + ". " + image_list[i])

                        option = int(input("Please enter an option. For example, 1\n"))

                        # valiate option ensure it fall into the range
                        if (option > 0 and option < image_list_length + 1):
                            result = query.upload_image(image_list[option - 1], self.__id_token)
                            print(result)

                        print("\n")
                        print("--------------------------------------------------------------")

                    # if user choose to add tages to an image
                    if (choice == "3"):
                        print("\nif user choose to add tages to an image")

                    # if user choose to delete an image
                    if (choice == "4"):
                        print("\nif user choose to delete an image")

                # if user has not signed in
                else:
                    self.__show_specific_menu("1")
                    print("\nPlease Sign In or Sign Up")
                    choice = input("Please enter an option. For example, 1\n")
                    if (choice == "1" or choice == "3"):
                        self.__id_token = authenticate.log_in()
                    if (choice == "2"):
                        self.__id_token = None

            # if a user selects quit menu
            if (choice == "4"):
                exit()


if __name__ == "__main__":
    menu = Menu()
    menu.menu_start()


