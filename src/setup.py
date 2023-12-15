""" module import """
from .routes.main import main


class SetupManager:
    """use setup class to integrate all component of the project """

    @classmethod
    def start_server(cls):
        """ start server """
        main()
