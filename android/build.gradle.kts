// Top-level build file where you can add configuration options common to all sub-projects/modules.

import org.gradle.api.tasks.Delete
import org.gradle.api.file.Directory

plugins {
    id("com.google.gms.google-services") version "4.4.3" apply false
    // Optional: apply necessary plugins
}

buildscript {
    repositories {
        google()
        mavenCentral()
    }

    dependencies {
        // Required for Firebase
        classpath("com.google.gms:google-services:4.4.1")
    }
}

allprojects {
    repositories {
        google()
        mavenCentral()
    }
}

// Optional: Move build directory outside module folder
val newBuildDir: Directory = rootProject.layout.buildDirectory.dir("../../build").get()
rootProject.layout.buildDirectory.set(newBuildDir)

subprojects {
    val newSubprojectBuildDir: Directory = newBuildDir.dir(project.name)
    project.layout.buildDirectory.set(newSubprojectBuildDir)
}

subprojects {
    project.evaluationDependsOn(":app")
}

// Clean task to remove build output
tasks.register<Delete>("clean") {
    delete(rootProject.layout.buildDirectory)
}
