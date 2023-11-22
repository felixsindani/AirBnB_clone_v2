#!/usr/bin/python3
'''
    Implementing the console for the HBnB project
'''
import cmd
import json
import shlex
from os import getenv
from models.base_model import BaseModel
from models import storage
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review


storage_type = getenv("HBNB_TYPE_STORAGE")

classes = {"Amenity": Amenity, "BaseModel": BaseModel, "City": City,
           "Place": Place, "Review": Review, "State": State, "User": User}


class HBNBCommand(cmd.Cmd):
    '''
        entry point to the console
    '''

    prompt = ("(hbnb) ")

    def do_quit(self, args):
        '''
            Quit command to exit the console.
        '''
        return True

    def do_EOF(self, args):
        '''
            Exits EOF
        '''
        print()
        return True

    def do_create(self, arg):
        '''
            Create i new instance of class BaseModel and saves it
            to the JSON file.
        '''
        args = arg.split()

        if len(args) == 0:
            print("** class name missing **")
            return

        new_args = []
        for i in args:
            idx = i.find("=")
            i = i[0: idx] + i[idx:].replace('_', ' ')
            new_args.append(i)

        if new_args[0] in classes:
            new_instance = classes[new_args[0]]()
            new_dictionary = {}
            for i in new_args:
                if i != new_args[0]:
                    new_list = i.split('=')
                    new_dictionary[new_list[0]] = new_list[1]

            for k, v in new_dictionary.items():
                if v[0] == '"':
                    variable_list = shlex.split(v)
                    new_dictionary[k] = variable_list[0]
                    setattr(new_instance, k, new_dictionary[k])
                else:
                    try:
                        if type(eval(v)).__name__ == 'int':
                            v = eval(v)
                    except:
                        continue
                    try:
                        if type(eval(str(v))).__name__ == 'float':
                            v = eval(v)
                    except:
                        continue
                    setattr(new_instance, k, v)
            new_instance.save()
            print(new_instance.id)
        else:
            print("** class doesn't exist **")

    def do_show(self, args):
        '''
            Print the string representation of an instance based on
            the class name and id given as args
        '''
        args = shlex.split(args)
        if len(args) == 0:
            print("** class name missing **")
            return
        if len(args) == 1:
            print("** instance id missing **")
            return
        obj_dict = storage.all()
        try:
            eval(args[0])
        except NameError:
            print("** class doesn't exist **")
            return
        key = args[0] + "." + args[1]
        key = args[0] + "." + args[1]
        try:
            value = obj_dict[key]
            print(value)
        except KeyError:
            print("** no instance found **")

    def do_destroy(self, args):
        '''
            Deletes an instance based on the class name and id
        '''
        args = shlex.split(args)
        if len(args) == 0:
            print("** class name missing **")
            return
        elif len(args) == 1:
            print("** instance id missing **")
            return
        class_name = args[0]
        class_id = args[1]
        obj_dict = storage.all()
        try:
            eval(class_name)
        except NameError:
            print("** class doesn't exist **")
            return
        key = class_name + "." + class_id
        try:
            del obj_dict[key]
        except KeyError:
            print("** no instance found **")
        storage.save()

    def do_all(self, args):
        '''
            Prints all string representation of all instances
        '''
        obj_list = []
        objects = storage.all()
        try:
            if len(args) != 0:
                eval(args)
        except NameError:
            print("** class doesn't exist **")
            return
        for key, val in objects.items():
            if len(args) != 0:
                if type(val) is eval(args):
                    obj_list.append(val)
            else:
                obj_list.append(val)

        print(obj_list)

    def do_update(self, args):
        '''
            Update an instance based on the class name and id as args
        '''
        args = shlex.split(args)
        if len(args) == 0:
            print("** class name missing **")
            return
        elif len(args) == 1:
            print("** instance id missing **")
            return
        elif len(args) == 2:
            print("** attribute name missing **")
            return
        elif len(args) == 3:
            print("** value missing **")
            return
        try:
            eval(args[0])
        except NameError:
            print("** class doesn't exist **")
            return
        key = args[0] + "." + args[1]
        obj_dict = storage.all()
        try:
            obj_value = obj_dict[key]
        except KeyError:
            print("** no instance found **")
            return
        try:
            attr_type = type(getattr(obj_value, args[2]))
            args[3] = attr_type(args[3])
        except AttributeError:
            pass
        setattr(obj_value, args[2], args[3])
        obj_value.save()

    def emptyline(self):
        '''
            Prevent printing when emptyline is passed
        '''
        pass

    def do_count(self, args):
        '''
            Counts number of instances
        '''
        obj_list = []
        objects = storage.all()
        try:
            if len(args) != 0:
                eval(args)
        except NameError:
            print("** class doesn't exist **")
            return
        for key, val in objects.items():
            if len(args) != 0:
                if type(val) is eval(args):
                    obj_list.append(val)
            else:
                obj_list.append(val)
        print(len(obj_list))

    def default(self, args):
        '''
            defines function not expicitly defined
        '''
        functions = {"all": self.do_all, "update": self.do_update,
                     "show": self.do_show, "count": self.do_count,
                     "destroy": self.do_destroy, "update": self.do_update}
        args = (args.replace("(", ".").replace(")", ".")
                .replace('"', "").replace(",", "").split("."))

        try:
            cmd_arg = args[0] + " " + args[2]
            func = functions[args[1]]
            func(cmd_arg)
        except:
            print("*** Unknown syntax:", args[0])


if __name__ == "__main__":
    '''
        Entry point for main loop
    '''
    HBNBCommand().cmdloop()
