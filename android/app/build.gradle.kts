plugins {
    id("com.android.application")
    id("kotlin-android")
    // The Flutter Gradle Plugin must be applied after the Android and Kotlin Gradle plugins.
    id("dev.flutter.flutter-gradle-plugin")
}

android {
    namespace = "com.example.phishzil"
    compileSdk = flutter.compileSdkVersion

    // ✅ Required NDK version for some dependencies (e.g. telephony, sms_advanced)
    ndkVersion = "27.0.12077973"

    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_11
        targetCompatibility = JavaVersion.VERSION_11
        // ✅ Enable Java 8+ desugaring support
        isCoreLibraryDesugaringEnabled = true
    }

    kotlinOptions {
        jvmTarget = JavaVersion.VERSION_11.toString()
    }

    defaultConfig {
        applicationId = "com.example.phishzil"
        // ✅ Ensure minSdk is at least 26 for desugaring support
        minSdk = maxOf(26, flutter.minSdkVersion)
        targetSdk = flutter.targetSdkVersion
        versionCode = flutter.versionCode
        versionName = flutter.versionName
    }

    buildTypes {
        release {
            signingConfig = signingConfigs.getByName("debug")
        }
    }
}

flutter {
    source = "../.."
}

// ✅ Dependencies section for desugaring support
dependencies {
    coreLibraryDesugaring("com.android.tools:desugar_jdk_libs:2.1.5")
}

// ✅ ADDITIONAL BUILD CONFIG BELOW

// 👇 Ensure all dependencies resolve properly
allprojects {
    repositories {
        google()
        mavenCentral()
    }
}

// 👇 Relocate build directories (optional but helpful in mono-repo structures)
val newBuildDir: Directory = rootProject.layout.buildDirectory.dir("../../build").get()
rootProject.layout.buildDirectory.value(newBuildDir)

subprojects {
    val newSubprojectBuildDir: Directory = newBuildDir.dir(project.name)
    project.layout.buildDirectory.value(newSubprojectBuildDir)
}

// ⚠️ DO NOT register "clean" again if it already exists in the root `build.gradle.kts`
// Uncomment below ONLY if it does not already exist.
// tasks.register<Delete>("clean") {
//     delete(rootProject.layout.buildDirectory)
// }
