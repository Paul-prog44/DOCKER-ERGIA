##################      INFO     #####################

Les commits fait sous le pseudo "00047988" ont été fait par Robin.

Les comptes de bases insérés automatiquement dans la base ont pour mot de passe : Password123!


################## CONFIGURATION #####################

    Commandes a executer:

        venv\Scripts\activate

        pip install -r requirements.txt

        Windows:

            $env:FLASK_APP = "flaskr/main"
            $env:FLASK_ENV = "development"
            $env:FLASK_DEBUG = 1
        Linux:
            export FLASK_APP="flaskr/main"
            export FLASK_ENV="development"
            export FLASK_DEBUG=1

        flask run

    Config database :
        Si ce n'est pas fait, quand vous tirez le projet il faut que vous vous fassiez votre propre fichier de conf dans
        le répertoire conf: il doit s'appeler config.ini et vous devez mettre dedans les champs contenus dans le fichier
        configexample.ini contenu dans le même répertoire et remplir les champs avec votre configuration de database.