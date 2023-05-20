def ascii():
    return (Colour.green("""                                   
  __  __  _____  _____ 
 |  \/  |/ ____|/ ____|
 | \  / | |  __| (___  
 | |\/| | | |_ |\___ \ 
 | |  | | |__| |____) |
 |_|  |_|\_____|_____/ 
                                                      
    """) + "(" +
            Colour.blue("v4") + ")" +
            Colour.red(" Auteurs: Maxime,Gregoire,Sacha") +
            "\n")


class Colour():
    @staticmethod
    def red(str):
        return "\033[91m" + str + "\033[0m"

    @staticmethod
    def green(str):
        return "\033[92m" + str + "\033[0m"

    @staticmethod
    def yellow(str):
        return "\033[93m" + str + "\033[0m"

    @staticmethod
    def blue(str):
        return "\033[94m" + str + "\033[0m"
