module.exports = function(grunt) {
  grunt.initConfig({
    appDir: 'app',

    bower: {
      install: {
        options: {
          targetDir: '<%= appDir %>/js/lib-bower',
          layout: 'byComponent',
          install: true,
          verbose: false,
          cleanTargetDir: true,
          cleanBowerDir: false,
          bowerOptions: {}
        }
      }
    }
  });

  grunt.loadNpmTasks('grunt-bower-task');

};
