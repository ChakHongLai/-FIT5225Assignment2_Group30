"""
This program is a part of "FIT5225 Cloud Computing and Security - A2 TagTag", a serverless demo. The whole project is composed of a client-side UI and a set of AWS cloud resources including aws-s3, dynamo, lambda, aws-api-gateway, aws-cognito. This program functions as a command-line interface interacting with aws-cognito and aws-api-gateway.

Author@Xicheng Wang
Email:xwan0255@student.monash.edu
"""
#!/bin/bash

import authenticate
import upload
import query



class Menu:
    
    def __init__(self):

        self.__items= { # menu items stand for all options available
            "1":{"1":["Authentication", "Sign In"], "2":["Authentication", "Sign Up"],"3":["Authentication", "Sign Out"]},
            "2":{"1":"Upload"},
            "3":{"1":["Query", "Seek Images By A List of Tags"], "2":["Query", "Seek Images By an Image"], "3":["Query", "Add Tags to a Cloud Image"], "4":["Query", "Delete Image By Id"], "5":["Query", "List All Images"]},
            "4":{"1":"Quit"}
        }
        
        # id_token 
        self.__id_token=None



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
        for o_index, sdict in self.__items.items():

            #jumping signal
            last_g_menu_item=""
            for i_index, menu_item in sdict.items():
                
                g_menu_item=""

                #if there is are sub-menus
                if(str(type(menu_item))=="<class 'list'>"):
                    g_menu_item=menu_item[0]

                #if there is no sub-menu
                if(str(type(menu_item))=="<class 'str'>"):
                    g_menu_item=menu_item
                
                if(g_menu_item!=last_g_menu_item):
                    print(o_index+". "+g_menu_item)
                    last_g_menu_item=g_menu_item

        print("\n")
        print("--------------------------------------------------------------")



    def __show_specific_menu(self, g_menu_id):

        print("-------------------------- Choice {} --------------------------".format(g_menu_id))
        print("\n")
        sdict=self.__items[g_menu_id]

        for i_index, menu_item in sdict.items():
            
            print(g_menu_id+"."+i_index+" "+menu_item[1])

        print("\n")
        print("--------------------------------------------------------------")



    def menu_start(self):

        #a menu loop 
        while(True):
            #show project info
            self.__show_program_info()

            #show primary menu
            self.__show_general_menu()

            g_choice=input("Please enter an option. For example, 1\n")

            #if a user selects authenticate menu
            if(g_choice=="1"):
                self.__show_specific_menu(g_choice)
                choice=input("Please enter an option. For example, 1\n")

                #if user choose sign in
                if(choice=="1"):
                    if(self.__id_token==None):
                        self.__id_token=authenticate.sign_in()
                    else:
                        print("\nYou have already signed in an account! Please sign out first")

                #if user choose to sign up
                if(choice=="2"):
                    if(self.__id_token==None):
                        self.__id_token=authenticate.sign_up()
                    else:
                        print("\nYou have already signed in an account! Please sign out first")

                #if user choose to sign out
                if(choice=="3" and self.__id_token!=None):
                    authenticate.sign_out(self.__id_token)
                    self.__id_token=None
                    print("\nUser has signed out!")

            #if a user selects upload menu 
            if(g_choice=="2"):
                #if user has signed in 
                if(self.__id_token!=None):
                    print("------------------------ Upload Folder ------------------------")
                    print("\n")       

                    image_list=upload.list_images()
                    image_list_length=len(image_list)
                    for i in range(image_list_length):
                        print("\n{0}:{1}".format(i, image_list[i]))

                    option=int(input("Please enter an option. For example, 1\n"))

                    #valiate option ensure it fall into the range 
                    if(option>=0 and option <image_list_length):
                        
                        result=upload.upload_image(image_list[option], self.__id_token)
                        print("\nupload result:{0}".format(result))

                    print("\n")
                    print("--------------------------------------------------------------")
                #if user has not signed in
                else:
                    self.__show_specific_menu("1")
                    print("\nPlease Sign In or Sign Up")
                    choice=input("Please enter an option. For example, 1\n")
                    if(choice=="1" or choice=="3"):
                        self.__id_token=authenticate.sign_in()
                    if(choice=="2"):
                        self.__id_token=None

            #if a user selects query menu
            if(g_choice=="3"):

                #if user has signed in 
                if(self.__id_token!=None):

                    self.__show_specific_menu(g_choice)
                    choice=input("Please enter an option. For example, 1\n")

                    #if user choose to seek images by tages
                    if(choice=="1"):

                        tags_str=input("\nplease input tags separated by comma")

                        tags=[]
                        for tag in tags_str.split(","):
                            tags.append(tag.strip())
                        print("\ntags:{0}".format(tags))
                        links=query.seek_images_by_tags(tags, self.__id_token)
                        if(links!=None and len(links)>0):
                            link_id=0
                            for link in links:
                                print("\n{0}:{1}".format(link_id, link))
                                link_id+=1
                        else:
                            print("\nempty list is returned!")

                    #if user choose to seek images by a image
                    if(choice=="2"):

                        print("------------------------ Upload Folder ------------------------")
                        print("\n")       

                        image_list=upload.list_images()
                        image_list_length=len(image_list)
                        for i in range(image_list_length):
                            print("\n{0}:{1}".format(i, image_list[i]))

                        option=int(input("Please enter an option. For example, 1\n"))

                        #valiate option ensure it fall into the range 
                        if(option>=0 and option <image_list_length):
                            
                            links=query.seek_images_by_image(image_list[option], self.__id_token)
                            if(links!=None and len(links)>0):
                                link_id=0
                                for link in links:
                                    print("\n{0}:{1}".format(link_id, link))
                                    link_id+=1
                            else:
                                print("\nempty list is returned!")

                        print("\n")
                        print("--------------------------------------------------------------")

                    #if user choose to add tages to an image
                    if(choice=="3"):

                        #get tags want to added from a user
                        tags_str=input("\nplease input tags separated by comma")
                        tags=[]
                        for tag in tags_str.split(","):
                            tags.append(tag.strip())
                        print("\ntags:{0}".format(tags))

                        #get an url to an image in aws-s3-bucket
                        links=query.get_all_images(self.__id_token)
                        if(links!=None and len(links)>0):
                            link_id=0
                            for link in links:
                                print("\n{0}:{1}".format(link_id, link))
                                link_id+=1
                            option=input("\nplease choose a link")
                            image_url=links[int(option)]
                            
                            #request to add
                            result=query.add_tags_to(tags, image_url, self.__id_token)
                            print("\n{0}".format(result))
                        else:
                            print("\nempty list is returned!")

                    #if user choose to delete an image
                    if(choice=="4"):

                        #get an url to an image in aws-s3-bucket
                        links=query.get_all_images(self.__id_token)
                        if(links!=None and len(links)>0):
                            link_id=0
                            for link in links:
                                print("\n{0}:{1}".format(link_id, link))
                                link_id+=1
                            option=input("\nplease choose a link")
                            image_url=links[int(option)]

                            #request to delete
                            query.delete_image(image_url, self.__id_token)
                        else:
                            print("\nempty list is returned!")

                    #if a user choose to list all images in aws-s3
                    if(choice=="5"):
                        links=query.get_all_images(self.__id_token)
                        if(links!=None and len(links)>0):
                            link_id=0
                            for link in links:
                                print("\n{0}:{1}".format(link_id, link))
                                link_id+=1
                        else:
                            print("\nempty list is returned!")
                   
                #if user has not signed in
                else:
                    self.__show_specific_menu("1")
                    print("\nPlease Sign In or Sign Up")
                    choice=input("Please enter an option. For example, 1\n")
                    if(choice=="1" or choice=="3"):
                        self.__id_token=authenticate.sign_in()
                    if(choice=="2"):
                        self.__id_token=None
            
            #if a user selects quit menu
            if(g_choice=="4"):

                exit()



if __name__ == "__main__":

    menu= Menu()
    menu.menu_start()


