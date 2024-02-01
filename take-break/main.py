from app_settings import general_settings, nodes_settings, speed_settings
from my_objects import ScreenSaver

def main():
    app = ScreenSaver(general_settings=general_settings, nodes_settings=nodes_settings, speed_settings=speed_settings)
    app.init_pygame()
    app.on_execute()
if __name__ == "__main__":
    main()
