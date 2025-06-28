plugins {
    id("com.android.application")
    id("kotlin-android")
    id("com.google.gms.google-services") // ✅ Required for Firebase
    id("dev.flutter.flutter-gradle-plugin")
}

android {
    namespace = "com.example.phishzil"
    compileSdk = flutter.compileSdkVersion

    ndkVersion = "27.0.12077973" // ✅ Needed for native Firebase plugins

    defaultConfig {
        applicationId = "com.example.phishzil"
        minSdk = maxOf(26, flutter.minSdkVersion) // ✅ Firebase needs minSdk 21+, most use 26+
        targetSdk = flutter.targetSdkVersion
        versionCode = flutter.versionCode
        versionName = flutter.versionName
    }

    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_11
        targetCompatibility = JavaVersion.VERSION_11
        isCoreLibraryDesugaringEnabled = true // ✅ Support for new Java features
    }

    kotlinOptions {
        jvmTarget = JavaVersion.VERSION_11.toString()
    }

    buildTypes {
        release {
            signingConfig = signingConfigs.getByName("debug") // change to release config for production
        }
    }
}

flutter {
    source = "../.."
}

dependencies {
    // ✅ Desugaring to support modern Java APIs on older Android
    coreLibraryDesugaring("com.android.tools:desugar_jdk_libs:2.1.5")

    // ✅ Firebase BoM for consistent dependency versions
    implementation(platform("com.google.firebase:firebase-bom:33.15.0"))

    // ✅ Firebase services — add more as needed
    implementation("com.google.firebase:firebase-analytics")         // Analytics
    implementation("com.google.firebase:firebase-auth")              // Auth
    implementation("com.google.firebase:firebase-firestore")         // Firestore
    implementation("com.google.firebase:firebase-messaging")         // Messaging
}

// ✅ Ensure repositories are correctly declared
allprojects {
    repositories {
        google()
        mavenCentral()
    }
}

// ✅ Optional: Relocate build folder if part of mono-repo
val newBuildDir: Directory = rootProject.layout.buildDirectory.dir("../../build").get()
rootProject.layout.buildDirectory.value(newBuildDir)

subprojects {
    val newSubprojectBuildDir: Directory = newBuildDir.dir(project.name)
    project.layout.buildDirectory.value(newSubprojectBuildDir)
}
