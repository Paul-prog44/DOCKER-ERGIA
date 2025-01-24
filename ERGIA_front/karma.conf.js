module.exports = function (config) {
    config.set({
      frameworks: ['jasmine', '@angular-devkit/build-angular'],
      plugins: [
        require('karma-jasmine'),
        require('karma-chrome-launcher'),
        require('karma-coverage'),
        require('@angular-devkit/build-angular/plugins/karma'),
      ],
      reporters: ['progress', 'coverage'],
      coverageReporter: {
        type: 'lcov', // Format LCOV
        dir: 'coverage/', // Dossier de sortie
        subdir: '.', // Tous les fichiers dans le même dossier
        
        exclude: [
          '/src/app/*.spec.ts',
          '/src/app/**/*.spec.ts'
        ]
      },
      browsers: ['ChromeHeadless'], // Pour une exécution en mode CI
      singleRun: true, // Quitter après l'exécution des tests
    });
  };