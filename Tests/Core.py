#Downloading ml assets from library folder
import sys
import os
sys.path.append(os.path.dirname(__file__))
import ML_assets as ml
import Architectures as arch
#Importing rest of the libraries

import tensorflow as tf
import matplotlib.pyplot as plt
import numpy as np
from timeit import default_timer as timer   
import pandas as pd
from sklearn.model_selection import train_test_split
from tqdm import tqdm
from contextlib import redirect_stdout

class Utils:
    
    def Initialize_data(DataBase_directory, Data_directory, img_H, img_W, grayscale, Load_from_CSV):
        """
        Initializes -> Loading data from main DataBase folder and load it by classes in 
        data directory

        Args:
            DataBase_directory (str):   Main DataBase directory
            Data_directory (str):       Local project resized/grayscaled DataBase directory
            img_H / img_W (int):        Image height and width in local DataBase
            grayscale (bool):           Grayscale or RGB 
            Load_from_CSV (bool):       Load data from CSV file instead of jpg/png...

        Returns:
            Database in project folder
        """    
        
        if not os.path.isdir(Data_directory):
            os.makedirs(Data_directory)
            print("Creating data storage directory...\n")
            
        if len(os.listdir(Data_directory)) == 0:
            print("There is no Dataset Initialized, initializing Dataset...")
            if Load_from_CSV:
                ml.DataSets.Create_Img_Classification_DataSet_CSV(DataBase_directory, img_H, img_W, Save_directory=Data_directory)
            else:
                ml.DataSets.Create_Img_Classification_DataSet(DataBase_directory, img_H, img_W, Save_directory=Data_directory , grayscale = grayscale)
        else:
            print("Found initialized Dataset")
            database_list = os.listdir(DataBase_directory)
            data_list = os.listdir(Data_directory)
            if Load_from_CSV:
                data_list = [element.replace(".csv" , "") for element in data_list] 
                database_list = ['sample_submission', 'x_test','x_train', 'y_test','y_train']
                
            data_list_clean = [element.replace(".npy" , "") for element in data_list] 
            
            
            if database_list != data_list_clean:
                print("Dataset is lacking some of the classes, initializing Dataset again")
                if Load_from_CSV:
                    ml.DataSets.Create_Img_Classification_DataSet_CSV(DataBase_directory, img_H, img_W, Save_directory=Data_directory)
                else:
                    ml.DataSets.Create_Img_Classification_DataSet(DataBase_directory, img_H, img_W, Save_directory=Data_directory , grayscale = grayscale)
            else:
                print("Dataset is initialized correctly!")
                   
    
    def Process_Data(x , y ,dataset_multiplier, DataProcessed_directory, Kaggle_set, flipRotate = False , randBright = False , gaussian = False , denoise = False , contour = False ):        
        #Folder creation if not existing
        if not os.path.isdir(DataProcessed_directory):
            os.makedirs(DataProcessed_directory)
            print("Creating processed data storage directory...\n") 
        #If folder exists trying to load data from it
        else:  
            print("Found processed Dataset,loading...")
            if not Kaggle_set:
                try:
                    x_train = np.load(os.path.join(DataProcessed_directory ,"x_train.npy"))
                    y_train = np.load(os.path.join(DataProcessed_directory ,"y_train.npy"))
                    
                    x_val = np.load(os.path.join(DataProcessed_directory ,"x_val.npy"))
                    y_val = np.load(os.path.join(DataProcessed_directory ,"y_val.npy"))
                    
                    x_test = np.load(os.path.join(DataProcessed_directory ,"x_test.npy"))
                    y_test = np.load(os.path.join(DataProcessed_directory ,"y_test.npy"))
                    return x_train , y_train , x_val , y_val , x_test , y_test
                    
                except:
                    print("Could not load processed files, probably not present in the folder, creating...")
                
            else:
                try:
                    x_train = np.load(os.path.join(DataProcessed_directory ,"x_train.npy"))
                    y_train = np.load(os.path.join(DataProcessed_directory ,"y_train.npy"))
                    
                    x_val = np.load(os.path.join(DataProcessed_directory ,"x_val.npy"))
                    y_val = np.load(os.path.join(DataProcessed_directory ,"y_val.npy"))
                    return x_train , y_train , x_val , y_val
        
                       
                except:
                    print("Could not load processed files, probably not present in the folder, creating...")
               
    
        print("There is no Dataset processed, processing Dataset...")

        if Kaggle_set:
            x_train , x_val , y_train , y_val = train_test_split(x,y,test_size = 0.2 ,stratify = y, shuffle = True)
        else:
            x_train , x_val , y_train , y_val = train_test_split(x,y,test_size = 0.3 ,stratify = y, shuffle = True)
            x_val , x_test , y_val , y_test = train_test_split(x_val,y_val,test_size = 0.66 ,stratify = y_val, shuffle = True)
        
        print("Augmentation of images...")
        if (not (flipRotate or randBright or gaussian or denoise or contour)) and dataset_multiplier >1:
            print("\nNo augmentation specified, dataset will be just multiplied",dataset_multiplier, "times")
            
        if (not (flipRotate or randBright or gaussian or denoise or contour)) and dataset_multiplier <=1:
            print("\nNo augmentation, skipping...")
        x_train,y_train = ml.DataSets.Augment_classification_dataset(x_train, y_train, dataset_multiplier, flipRotate, randBright, gaussian, denoise, contour )            
            
        
        
        
        if not Kaggle_set:
            np.save(os.path.join(DataProcessed_directory ,"x_train.npy") , x_train)
            np.save(os.path.join(DataProcessed_directory ,"y_train.npy") , y_train)
            
            np.save(os.path.join(DataProcessed_directory ,"x_val.npy") , x_val)
            np.save(os.path.join(DataProcessed_directory ,"y_val.npy") , y_val)
            
            np.save(os.path.join(DataProcessed_directory ,"x_test.npy") , x_test)
            np.save(os.path.join(DataProcessed_directory ,"y_test.npy") , y_test)
            
            return x_train , y_train , x_val , y_val , x_test , y_test
            
        else:
            np.save(os.path.join(DataProcessed_directory ,"x_train.npy") , x_train)
            np.save(os.path.join(DataProcessed_directory ,"y_train.npy") , y_train)
            
            np.save(os.path.join(DataProcessed_directory ,"x_val.npy") , x_val)
            np.save(os.path.join(DataProcessed_directory ,"y_val.npy") , y_val)
            
            return x_train , y_train , x_val , y_val
    
    
    def Initialize_model(model_architecture, n_classes, img_H, img_W, channels, show_architecture):    
      
        #!!! Defining the architecture of the CNN 
        #and creation of directory based on it and initial parameters
        #########################################################################
        #########################################################################
        
        #Checking if given architecture name is present in library
        model_architecture = f"{model_architecture}"
        
        model_architecture_class = getattr(arch.Img_Classification, model_architecture, None)
        
        if model_architecture_class is not None:
            # If the class is found, instantiate the model
            model = model_architecture_class((img_H,img_W,channels) , n_classes)
            print("Found architecture named: ",model_architecture,)
        else:
            # If the class is not found, print a message
            model = None
            print("No such model architecture in library")
        
        #!!! Building and compiling model
        #########################################################################
        #########################################################################
        #Choosing optimizer
        optimizer = tf.keras.optimizers.Adam()
        #Compiling model
        model.compile(optimizer=optimizer, loss='categorical_crossentropy', metrics=['accuracy'])
        if show_architecture:
            model.summary()
        
        #########################################################################
        #########################################################################
        return model
    
    def Initialize_Gan_model(generator_arch, discriminator_arch, latent_dim, show_architecture):    
        g_arch = f"{generator_arch}"
        d_arch = f"{discriminator_arch}"
        generator_class = getattr(arch.Gan, g_arch, None)
        discriminator_class = getattr(arch.Gan, d_arch, None)
        
        if (generator_class and discriminator_class) is not None:
            gan_generator = generator_class(latent_dim)
            gan_discriminator = discriminator_class()
            print("Found generator named: ",g_arch,"\nFound discriminator named: ",d_arch)
        else:
            if generator_class is None:
                print("Could not find generator class named: ",g_arch)
            if discriminator_class is None:
                print("Could not find discriminator class named: ",d_arch)
                
        gan_discriminator.compile(loss='binary_crossentropy', optimizer=tf.keras.optimizers.Adam(0.0002, 0.5), metrics=['accuracy'])

        # make weights in the discriminator not trainable
        gan_discriminator.trainable = False
        # connect them
        gan_model = tf.keras.Sequential()
        # add generator
        gan_model.add(gan_generator)
        # add the discriminator
        gan_model.add(gan_discriminator)
        gan_model.compile(loss='binary_crossentropy', optimizer=tf.keras.optimizers.Adam(0.0002, 0.5))
        
        return gan_model, gan_generator, gan_discriminator
            

    #Saving progress each n epochs to folder
    def save_plot(examples,directory, epoch, n=10):
        # plot images
        for i in range(n * n):
            # define subplot
            plt.subplot(n, n, 1 + i)
            # turn off axis
            plt.axis('off')
            # plot raw pixel data
            plt.imshow(examples[i, :, :])
            # save plot to file
        filename = os.path.join(directory, 'Epoch_%03d.png' %epoch )
    
        plt.savefig(filename)
        plt.close()
        
    def Initialize_weights_and_training(x_train, y_train, model, model_directory, model_architecture, train, epochs, patience, batch_size,min_delta, x_val=None, y_val=None, device = "CPU:0"):    
        #!!! Model training
        #########################################################################
        #########################################################################
        #Check if directory of trained model is present, if not, create one 
        if not os.path.isdir(model_directory):
            os.makedirs(model_directory)
            print("Creating model directory storage directory...\n")
            
        model_name = str(model_architecture + "_bs"+str(batch_size)+".keras")
        model_weights_directory = os.path.join(model_directory , model_name)
        model_history_directory = os.path.join(model_directory , "Model_history.csv")
        
        model , train , starting_epoch = ml.General.Load_model_check_training_progress(model, train, model_weights_directory, model_history_directory)
        
    
             
        if train:
            #Create callback function to save best performing model
            
            if starting_epoch == 0:
                csv_append = False
            else:
                csv_append = True
                
            callbacks = [
                        #Stop if no increase in accuracy after x epochs
                        tf.keras.callbacks.EarlyStopping(patience=patience, 
                                                         monitor='val_accuracy',
                                                         min_delta=min_delta),
                        #Checkpoint model if performance is increased
                        tf.keras.callbacks.ModelCheckpoint(filepath = model_weights_directory  ,
                                                        monitor = "val_accuracy",
                                                        save_best_only = True,
                                                        verbose = 1),
                        #Save data through training
                        tf.keras.callbacks.CSVLogger(filename = model_history_directory , append = csv_append)
                        ]
         
            with tf.device(device):
                
                #Start measuring time
                timer_start = timer()
                model.fit(x_train,y_train,
                          initial_epoch = starting_epoch,
                          validation_data = (x_val , y_val),
                          epochs=epochs,
                          batch_size = batch_size,
                          callbacks = callbacks
                          )
                
                print("Time took to train model: ",round(timer()-timer_start),2)    
                
            
            #Save the best achieved model
            print("Loading model which was performing best during training...\n")
            model.load_weights(model_weights_directory)   
                
        
             
         
            
         
        #########################################################################
        #########################################################################
        return model
    

    def Initialize_weights_and_training_gan(dataset, gan_model, gan_generator, gan_discriminator, train, generator_architecture, discriminator_architecture, model_directory, epochs, batch_size, latent_dim, sample_interval,device = "CPU:0"):
        #Check if directory of trained model is present, if not, create one 
        if not os.path.isdir(model_directory):
            os.makedirs(model_directory)
            print("Creating model directory storage directory...\n")
        model_architecture = str(str(generator_architecture)+" __ "+str(discriminator_architecture))        
        model_name = str(model_architecture + "_bs"+str(batch_size)+".keras")
        model_weights_directory = os.path.join(model_directory , model_name)
        model_history_directory = os.path.join(model_directory , "Model_history.csv")
        
        model , train , starting_epoch = ml.General.Load_model_check_training_progress(gan_model, train, model_weights_directory, model_history_directory)
        
        
             
        if train:
            #Create callback function to save best performing model
            
            if starting_epoch == 0:
                csv_append = False
            else:
                csv_append = True
                
            timer_start = timer()
            with tf.device(device):
                for epoch in range(epochs):
                    print("\nEpoch:",epoch)
                    steps_per_epoch = len(dataset) // batch_size
                    for step in tqdm(range(steps_per_epoch)):
                        with redirect_stdout(open(os.devnull, 'w')):
                            #1
                            #Taking batch of real samples from dataset
                            x_real, y_real = ml.General.generate_real_samples(dataset, batch_size//2)
                            
                            #2
                            #Generating batch of fake samples from generator
                            x_fake , y_fake = ml.General.generate_fake_samples(gan_generator, latent_dim, batch_size//2)
                            
                            #3
                            #Preparing combined real-fake set for discriminator to train
                            x = np.vstack((x_real,x_fake))
                            y = np.vstack((y_real, y_fake))
                            
                            #4
                            #Training discriminator
                            discriminator_loss = gan_discriminator.train_on_batch(x,y)
                            
                            #5
                            #Update generator via discriminator error
                            noise = np.random.normal(0, 1, (batch_size, latent_dim))
                            ones = np.ones((batch_size, 1))
                            generator_loss = gan_model.train_on_batch(noise, ones)
                            
                            #gan_callback()
                    # Print the progress
                    sys.stdout.write(f"[D loss: {discriminator_loss[0]:.3f} | D acc: {discriminator_loss[1]:.3f}] [G loss: {generator_loss:.3f}]")    
                   
                    # Save generated images every sample_interval
                    if epoch % sample_interval == 0:
                        print('save Plot, epoch:',epoch)
                        Utils.save_plot(x_fake,"Images",epoch,8)
                
                
                print("Time took to train model: ",round(timer()-timer_start),2)    
                
            
            #Save the best achieved model
            print("Loading model which was performing best during training...\n")
            model.load_weights(model_weights_directory)   


            return model
        
            

       
    def Initialize_Results(model,model_directory, dictionary,evaluate, x_train = None ,y_train = None ,x_val = None , y_val = None , x_test = None , y_test = None):    
        #!!! Model results
        #########################################################################
        #########################################################################
        
        #Plot model training history
        model_history_directory = os.path.join(model_directory , "Model_history.csv")
        Model_history = pd.read_csv(model_history_directory)
        ml.General.Model_training_history_plot_CSV(Model_history)
        
        
        try:
            #Create confusion matrix
            #Predict classes
            print("\nPredicting classes based on test set...")
            y_pred = model.predict(x_test)
            
            plt.figure()
            ml.General.Conf_matrix_classification(y_test  ,y_pred , dictionary , normalize = True)
        except:
            print("No test set provided, skipping...")
            
        try:
            #Create confusion matrix
            #Predict classes
            print("\nPredicting classes based on validation set...")
            y_pred = model.predict(x_val)
            
            plt.figure()
            ml.General.Conf_matrix_classification(y_val ,y_pred , dictionary , normalize = True)
        except:
            print("No validation set provided, skipping...")    
        
    
        if evaluate:
            try:
                #Evaluate model
                print("\nModel evaluation train set:")
                model.evaluate(x_train, y_train)
            except:
                print("No train set provided, skipping...")
                
            try:
                #Evaluate model
                print("\nModel evaluation validation set:")
                model.evaluate(x_val, y_val)
            except:
                print("No validation set provided, skipping...")
            
            try:
                #Evaluate model
                print("\nModel evaluation test set:")
                model.evaluate(x_test, y_test)
            except:
                print("No test set provided, skipping...")

class Project:
    class Classification_Project:
        def  __init__(self,config):
            #Low level constants
            self.PROJECT_DIRECTORY = os.path.dirname(os.path.abspath(sys.argv[0]))
            #Initial
            self.DATABASE_DIRECTORY = config.Initial_params["DataBase_directory"]
            self.KAGGLE_SET = config.Initial_params["Kaggle_set"]
            self.CSV_LOAD = config.Initial_params["Load_from_CSV"]
            self.IMG_H = config.Initial_params["img_H"]
            self.IMG_W = config.Initial_params["img_W"]
            self.GRAYSCALE= config.Initial_params["grayscale"]
            self.DATA_TYPE = config.Initial_params["DataType"]
            
            #Augment
            self.REDUCED_SET_SIZE = config.Augment_params["reduced_set_size"]
            self.DATASET_MULTIPLIER = config.Augment_params["dataset_multiplier"]
            self.FLIPROTATE = config.Augment_params["flipRotate"]
            self.RANDBRIGHT = config.Augment_params["randBright"]
            self.GAUSSIAN = config.Augment_params["gaussian_noise"]
            self.DENOISE = config.Augment_params["denoise"]
            self.CONTOUR = config.Augment_params["contour"]
            
            #Model
            self.MODEL_ARCHITECTURE = config.Model_parameters["model_architecture"]
            self.SHOW_ARCHITECTURE = config.Model_parameters["show_architecture"]
            self.DEVICE = config.Model_parameters["device"]
            self.TRAIN = config.Model_parameters["train"]
            self.EPOCHS = config.Model_parameters["epochs"]
            self.PATIENCE = config.Model_parameters["patience"]
            self.BATCH_SIZE = config.Model_parameters["batch_size"]
            self.MIN_DELTA = config.Model_parameters["min_delta"]
            self.EVALUATE = config.Model_parameters["evaluate"]
            
            #High level constants
            #Form
            self.FORM = "Grayscale" if self.GRAYSCALE else "RGB"
            #Channels
            self.CHANNELS = 3 if self.FORM == "RGB" else 1
            self.CHANNELS = self.CHANNELS+1 if self.CONTOUR else self.CHANNELS
    
            cr = 0 if self.REDUCED_SET_SIZE is None else self.REDUCED_SET_SIZE
            self.PARAM_MARK = "_m"+str(self.DATASET_MULTIPLIER)+"_cr"+str(cr)+"_"+ "_".join(["1" if x else "0" for x in [self.FLIPROTATE, self.RANDBRIGHT, self.GAUSSIAN, self.DENOISE, self.CONTOUR]])
    
                    
            self.DATA_DIRECTORY = os.path.join(self.PROJECT_DIRECTORY , "DataSet" , str(str(self.IMG_H)+"x"+str(self.IMG_W)+"_"+self.FORM))
            self.DATAPROCESSED_DIRECTORY = os.path.join(self.PROJECT_DIRECTORY , "DataSet_Processed" , str(str(self.IMG_H)+"x"+str(self.IMG_W)+"_"+self.FORM),self.PARAM_MARK)
            self.MODEL_DIRECTORY =  os.path.join(self.PROJECT_DIRECTORY , "Models_saved" , str(self.MODEL_ARCHITECTURE) , self.FORM , str(str(self.IMG_H)+"x"+str(self.IMG_W)) , str("bs"+str(self.BATCH_SIZE) + self.PARAM_MARK)  )
            
            
            
            
        def __str__(self):
            return f"This is class representing the project, main parameters are:\n\nOriginalDatabase: {self.DATABASE_DIRECTORY}\nArchitecture Used: {self.MODEL_ARCHITECTURE}"
            
    
        def Initialize_data(self): 
            """Initializing dataset from main database folder with photos to project folder in numpy format. Photos are 
            Resized and cropped without loosing much aspect ratio, r parameter decides above what proportions of edges 
            image will be cropped to square instead of squeezed""" 
            
            Utils.Initialize_data(self.DATABASE_DIRECTORY, self.DATA_DIRECTORY, self.IMG_H, self.IMG_W, self.GRAYSCALE , self.CSV_LOAD)
            ########################################################
        def Load_and_merge_data(self):
            """Loading dataset to memory from data directory in project folder, sets can be reduced to equal size
            to eliminate disproportions if they are not same size at the main database
            In this module dictionary with names of classes is created as well, names are based on names of datsets
            Datasets names are based on the folder names in main database folder"""
            
            self.X_TRAIN, self.Y_TRAIN, self.DICTIONARY = ml.DataSets.Load_And_Merge_DataSet(self.DATA_DIRECTORY , self.REDUCED_SET_SIZE )
            self.N_CLASSES = len(self.DICTIONARY)
            ########################################################
            
        def Process_data(self):
            #3
            ########################################################
            if self.KAGGLE_SET:
                self.X_TRAIN , self.Y_TRAIN, self.X_VAL , self.Y_VAL = Utils.Process_Data(self.X_TRAIN, self.Y_TRAIN, self.DATASET_MULTIPLIER, self.DATAPROCESSED_DIRECTORY, self.KAGGLE_SET, self.FLIPROTATE, self.RANDBRIGHT, self.GAUSSIAN, self.DENOISE, self.CONTOUR)
            
            else:
                self.X_TRAIN , self.Y_TRAIN, self.X_VAL , self.Y_VAL , self.X_TEST , self.Y_TEST = Utils.Process_Data(self.X_TRAIN, self.Y_TRAIN, self.DATASET_MULTIPLIER, self.DATAPROCESSED_DIRECTORY, self.KAGGLE_SET, self.FLIPROTATE, self.RANDBRIGHT, self.GAUSSIAN, self.DENOISE, self.CONTOUR)
            
            try:
                self.X_TRAIN = np.array(self.X_TRAIN/255 , dtype = self.DATA_TYPE)
                self.Y_TRAIN = np.array(self.Y_TRAIN , dtype = self.DATA_TYPE)
                
                self.X_VAL = np.array(self.X_VAL/255 , dtype = self.DATA_TYPE)
                self.Y_VAL = np.array(self.Y_VAL , dtype = self.DATA_TYPE)
                
                self.X_TEST = np.array(self.X_TEST/255 , dtype = self.DATA_TYPE)
                self.Y_TEST = np.array(self.Y_TEST , dtype = self.DATA_TYPE)
            except Exception as e:
                print("Could not standarize data:",e)
            
            
            ########################################################
            
    
        def Initialize_model_from_library(self):
            #4
            ########################################################
            self.MODEL = Utils.Initialize_model(model_architecture = self.MODEL_ARCHITECTURE,
                                        n_classes = self.N_CLASSES,
                                        img_H = self.IMG_H,
                                        img_W = self.IMG_W,
                                        channels = self.CHANNELS,
                                        show_architecture = self.SHOW_ARCHITECTURE
                                        )
            ########################################################
    
    
        def Initialize_weights_and_training(self, precompiled_model=None):
            #5
            ########################################################
            if precompiled_model:
                # Use the provided precompiled model
                self.MODEL = precompiled_model
            else:
                # Use the initialized model from Initialize_model function
                assert hasattr(self, 'MODEL'), "Model not initialized. Call Initialize_model_from_library first or use custom compiled model, f.e, from keras or your own."
            
                
                
            self.MODEL = Utils.Initialize_weights_and_training(x_train = self.X_TRAIN,
                                                       y_train= self.Y_TRAIN,
                                                       x_val = self.X_VAL,
                                                       y_val = self.Y_VAL,
                                                       model = self.MODEL,
                                                       model_directory = self.MODEL_DIRECTORY,
                                                       model_architecture = self.MODEL_ARCHITECTURE,
                                                       train = self.TRAIN,
                                                       epochs = self.EPOCHS,
                                                       patience = self.PATIENCE,
                                                       batch_size = self.BATCH_SIZE,
                                                       min_delta= self.MIN_DELTA,
                                                       device = self.DEVICE
                                                       )
            ########################################################
    
        def Initialize_resulits(self):
            #6
            ########################################################
            Utils.Initialize_Results(self.MODEL,
                                  self.MODEL_DIRECTORY,
                                  self.DICTIONARY,
                                  self.EVALUATE,
                                  self.X_TRAIN,
                                  self.Y_TRAIN,
                                  self.X_VAL,
                                  self.Y_VAL,
                                  self.X_TEST,
                                  self.Y_TEST
                                  )
            ######################################################## 
            
        def Generate_sample_submission(self, filepath = None):
            if filepath is None:
                sample_submission = pd.read_csv(os.path.join(self.DATA_DIRECTORY , "sample_submission.csv")) 

            #img_id = sample_submission.columns[0]
            label = sample_submission.columns[1]
            try:
                label_array = np.argmax(self.MODEL.predict(self.X_TEST), axis = 1)
            except:
                label_array = self.Y_TEST
            sample_submission[label] = label_array
            return sample_submission
    




    
    class Gan_Project:
        def  __init__(self,config):
            #Low level constants
            self.PROJECT_DIRECTORY = os.path.dirname(os.path.abspath(sys.argv[0]))
            #Initial
            self.DATABASE_DIRECTORY = config.Initial_params["DataBase_directory"]
            self.KAGGLE_SET = config.Initial_params["Kaggle_set"]
            self.CSV_LOAD = config.Initial_params["Load_from_CSV"]
            self.IMG_H = config.Initial_params["img_H"]
            self.IMG_W = config.Initial_params["img_W"]
            self.GRAYSCALE= config.Initial_params["grayscale"]
            self.DATA_TYPE = config.Initial_params["DataType"]
            
            #Augment
            self.REDUCED_SET_SIZE = config.Augment_params["reduced_set_size"]
            self.DATASET_MULTIPLIER = config.Augment_params["dataset_multiplier"]
            self.FLIPROTATE = config.Augment_params["flipRotate"]
            self.RANDBRIGHT = config.Augment_params["randBright"]
            self.GAUSSIAN = config.Augment_params["gaussian_noise"]
            self.DENOISE = config.Augment_params["denoise"]
            self.CONTOUR = config.Augment_params["contour"]
            
            #Model
            self.GENERATOR_ARCHITECTURE = config.Model_parameters["generator_architecture"]
            self.DISCRIMINATOR_ARCHITECTURE = config.Model_parameters["discriminator_architecture"]
            self.SHOW_ARCHITECTURE = config.Model_parameters["show_architecture"]
            self.DEVICE = config.Model_parameters["device"]
            self.TRAIN = config.Model_parameters["train"]
            self.EPOCHS = config.Model_parameters["epochs"]
            #self.PATIENCE = config.Model_parameters["patience"]
            self.LATENT_DIM = config.Model_parameters["latent_dim"]
            self.BATCH_SIZE = config.Model_parameters["batch_size"]
            self.SAMPLE_INTERVAL = config.Model_parameters["sample_interval"]
            #self.MIN_DELTA = config.Model_parameters["min_delta"]
            self.EVALUATE = config.Model_parameters["evaluate"]
            
            #High level constants
            #Form
            self.FORM = "Grayscale" if self.GRAYSCALE else "RGB"
            #Channels
            self.CHANNELS = 3 if self.FORM == "RGB" else 1
            self.CHANNELS = self.CHANNELS+1 if self.CONTOUR else self.CHANNELS
            
            cr = 0 if self.REDUCED_SET_SIZE is None else self.REDUCED_SET_SIZE
            self.PARAM_MARK = "_m"+str(self.DATASET_MULTIPLIER)+"_cr"+str(cr)+"_"+ "_".join(["1" if x else "0" for x in [self.FLIPROTATE, self.RANDBRIGHT, self.GAUSSIAN, self.DENOISE, self.CONTOUR]])
    
                    
            self.DATA_DIRECTORY = os.path.join(self.PROJECT_DIRECTORY , "DataSet" , str(str(self.IMG_H)+"x"+str(self.IMG_W)+"_"+self.FORM))
            self.DATAPROCESSED_DIRECTORY = os.path.join(self.PROJECT_DIRECTORY , "DataSet_Processed" , str(str(self.IMG_H)+"x"+str(self.IMG_W)+"_"+self.FORM),self.PARAM_MARK)
            self.MODEL_DIRECTORY =  os.path.join(self.PROJECT_DIRECTORY , "Models_saved" , str(str(self.GENERATOR_ARCHITECTURE)+" __ "+str(self.DISCRIMINATOR_ARCHITECTURE)) , self.FORM , str(str(self.IMG_H)+"x"+str(self.IMG_W)) , str("bs"+str(self.BATCH_SIZE) + self.PARAM_MARK)  )
            
        ########################################################    
            
        def __str__(self):
            return f"This is class representing the project, main parameters are:\n\nOriginalDatabase: {self.DATABASE_DIRECTORY}\nGenerator Used: {self.GENERATOR_ARCHITECTURE}\nDiscriminator Used: {self.DISCRIMINATOR_ARCHITECTURE}"
            
        ########################################################
    
        def Initialize_data(self): 
            """Initializing dataset from main database folder with photos to project folder in numpy format. Photos are 
            Resized and cropped without loosing much aspect ratio, r parameter decides above what proportions of edges 
            image will be cropped to square instead of squeezed""" 
            
            Utils.Initialize_data(DataBase_directory = self.DATABASE_DIRECTORY, 
                                  Data_directory = self.DATA_DIRECTORY, 
                                  img_H = self.IMG_H, 
                                  img_W = self.IMG_W, 
                                  grayscale = self.GRAYSCALE, 
                                  Load_from_CSV = self.CSV_LOAD
                                  )
            
        ########################################################
        
        def Load_and_merge_data(self):
            """Loading dataset to memory from data directory in project folder, sets can be reduced to equal size
            to eliminate disproportions if they are not same size at the main database
            In this module dictionary with names of classes is created as well, names are based on names of datsets
            Datasets names are based on the folder names in main database folder"""
            if not self.KAGGLE_SET:
                self.X_TRAIN, self.Y_TRAIN, self.DICTIONARY = ml.DataSets.Load_And_Merge_DataSet(self.DATA_DIRECTORY , self.REDUCED_SET_SIZE )
                self.N_CLASSES = len(self.DICTIONARY)
                
            else:
                self.X_TRAIN = np.load(os.path.join(self.DATA_DIRECTORY , "x_train.npy"))
                self.Y_TRAIN = np.load(os.path.join(self.DATA_DIRECTORY , "y_train.npy"))
                
                self.X_TEST = np.load(os.path.join(self.DATA_DIRECTORY , "x_test.npy"))
                try:
                    self.Y_TEST = np.load(os.path.join(self.DATA_DIRECTORY , "y_test.npy"))
                except:
                    self.Y_TEST = np.load(os.path.join(self.DATA_DIRECTORY , "y_test.npy"),allow_pickle = True)
                
        ########################################################
            
        def Process_data(self):

            if self.KAGGLE_SET:
                self.X_TRAIN , self.Y_TRAIN, self.X_VAL , self.Y_VAL = Utils.Process_Data(x = self.X_TRAIN,
                                                                                          y = self.Y_TRAIN,
                                                                                          dataset_multiplier = self.DATASET_MULTIPLIER,
                                                                                          DataProcessed_directory = self.DATAPROCESSED_DIRECTORY,
                                                                                          Kaggle_set = self.KAGGLE_SET,
                                                                                          flipRotate = self.FLIPROTATE,
                                                                                          randBright = self.RANDBRIGHT,
                                                                                          gaussian = self.GAUSSIAN,
                                                                                          denoise = self.DENOISE,
                                                                                          contour = self.CONTOUR
                                                                                          )

            else:
                self.X_TRAIN , self.Y_TRAIN, self.X_VAL , self.Y_VAL , self.X_TEST , self.Y_TEST = Utils.Process_Data(x = self.X_TRAIN,
                                                                                                                      y = self.Y_TRAIN,
                                                                                                                      dataset_multiplier = self.DATASET_MULTIPLIER,
                                                                                                                      DataProcessed_directory = self.DATAPROCESSED_DIRECTORY,
                                                                                                                      Kaggle_set = self.KAGGLE_SET,
                                                                                                                      flipRotate = self.FLIPROTATE,
                                                                                                                      randBright = self.RANDBRIGHT,
                                                                                                                      gaussian = self.GAUSSIAN,
                                                                                                                      denoise = self.DENOISE,
                                                                                                                      contour = self.CONTOUR
                                                                                                                      )
            
            try:
                self.X_TRAIN = np.array((self.X_TRAIN/255-0.5)*2 , dtype = self.DATA_TYPE)
                self.Y_TRAIN = np.array(self.Y_TRAIN , dtype = self.DATA_TYPE)
                
                self.X_VAL = np.array((self.X_VAL/255-0.5)*2 , dtype = self.DATA_TYPE)
                self.Y_VAL = np.array(self.Y_VAL , dtype = self.DATA_TYPE)
                
                self.X_TEST = np.array((self.X_TEST/255-0.5)*2 , dtype = self.DATA_TYPE)
                self.Y_TEST = np.array(self.Y_TEST , dtype = self.DATA_TYPE)
            except Exception as e:
                print("Could not standarize data:",e)
                
            
        ########################################################
        
            
        def Initialize_model_from_library(self):
            self.MODEL,self.GENERATOR,self.DISCRIMINATOR = Utils.Initialize_Gan_model(generator_arch = self.GENERATOR_ARCHITECTURE,
                                                                                      discriminator_arch = self.DISCRIMINATOR_ARCHITECTURE,
                                                                                      latent_dim = self.LATENT_DIM,
                                                                                      show_architecture = self.SHOW_ARCHITECTURE
                                                                                      )
            
            ########################################################
    
        def Initialize_weights_and_training_gan(self, precompiled_model=None):
            #5
            ########################################################
            if precompiled_model:
                # Use the provided precompiled model
                self.MODEL = precompiled_model
            else:
                # Use the initialized model from Initialize_model function
                assert hasattr(self, 'MODEL'), "Model not initialized. Call Initialize_model_from_library first or use custom compiled model, f.e, from keras or your own."
            
            self.MODEL = Utils.Initialize_weights_and_training_gan(dataset = self.X_TRAIN,
                                                                   gan_model = self.MODEL,
                                                                   gan_generator = self.GENERATOR,
                                                                   gan_discriminator = self.DISCRIMINATOR,
                                                                   train = self.TRAIN,
                                                                   generator_architecture = self.GENERATOR_ARCHITECTURE,
                                                                   discriminator_architecture = self.DISCRIMINATOR_ARCHITECTURE,
                                                                   model_directory = self.MODEL_DIRECTORY,
                                                                   epochs = self.EPOCHS,
                                                                   batch_size = self.BATCH_SIZE,
                                                                   latent_dim = self.LATENT_DIM,
                                                                   sample_interval = self.SAMPLE_INTERVAL,
                                                                   device = self.DEVICE
                                                                   )
                                

        def Initialize_resulits(self):
            #6
            ########################################################
            Utils.Initialize_Results(self.MODEL,
                                  self.MODEL_DIRECTORY,
                                  self.DICTIONARY,
                                  self.EVALUATE,
                                  self.X_TRAIN,
                                  self.Y_TRAIN,
                                  self.X_VAL,
                                  self.Y_VAL,
                                  self.X_TEST,
                                  self.Y_TEST
                                  )
            ######################################################## 
            
        def Generate_sample_submission(self, filepath = None):
            if filepath is None:
                sample_submission = pd.read_csv(os.path.join(self.DATA_DIRECTORY , "sample_submission.csv")) 
    
            #img_id = sample_submission.columns[0]
            label = sample_submission.columns[1]
            try:
                label_array = np.argmax(self.MODEL.predict(self.X_TEST), axis = 1)
            except:
                label_array = self.Y_TEST
            sample_submission[label] = label_array
            return sample_submission