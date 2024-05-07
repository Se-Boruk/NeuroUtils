#Downloading ml assets from library folder
import ML_assets as ml
import Architectures as arch
#Importing rest of the libraries
import os
import tensorflow as tf
import matplotlib.pyplot as plt
import numpy as np
from timeit import default_timer as timer   
import pandas as pd
from sklearn.model_selection import train_test_split





def Initialize_data(DataBase_directory, Data_directory, img_H, img_W, grayscale):

    
    if not os.path.isdir(Data_directory):
        os.makedirs(Data_directory)
        print("Creating data storage directory...\n")
        
    if len(os.listdir(Data_directory)) == 0:
        print("There is no Dataset Initialized, initializing Dataset...")
        ml.DataSets.Create_Img_Classification_DataSet(DataBase_directory, img_H, img_W, Save_directory=Data_directory , grayscale = grayscale)
    else:
        print("Found initialized Dataset")
        database_list = os.listdir(DataBase_directory)
        data_list = os.listdir(Data_directory)
        data_list_clean = [element.replace(".npy" , "") for element in data_list] 

        if database_list != data_list_clean:
            print("Dataset is lacking some of the classes, initializing Dataset again")
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
    print("Augmentation of images...")
    if not (flipRotate and randBright and gaussian and denoise and contour) and dataset_multiplier >1:
        print("\nNo augmentation specified, dataset will be just multiplied",dataset_multiplier, "times")
        
    if not (flipRotate and randBright and gaussian and denoise and contour) and dataset_multiplier <1:
        print("\nNo augmentation, skipping...")
    x,y = ml.DataSets.Augment_classification_dataset(x, y, dataset_multiplier, flipRotate, randBright, gaussian, denoise, contour )            
    
    if Kaggle_set:
        x_train , x_val , y_train , y_val = train_test_split(x,y,test_size = 0.2 ,stratify = y, shuffle = True)
    else:
        x_train , x_val , y_train , y_val = train_test_split(x,y,test_size = 0.3 ,stratify = y, shuffle = True)
        x_val , x_test , y_val , y_test = train_test_split(x_val,y_val,test_size = 0.66 ,stratify = y_val, shuffle = True)
        
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
    
def Initialize_weights_and_training(x_train, y_train, model, model_directory, model_architecture, train, epochs, patience, batch_size, x_val=None, y_val=None, device = "CPU:0"):    
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
                                                     min_delta=0.01),
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
        print("Predicting classes based on test set...")
        y_pred = model.predict(x_test)
        
        plt.figure()
        ml.General.Conf_matrix_classification(y_test  ,y_pred , dictionary , normalize = True)
    except:
        print("No test set provided, skipping...")
        
    try:
        #Create confusion matrix
        #Predict classes
        print("Predicting classes based on validation set...")
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
    
    
    #########################################################################
    #########################################################################

 
    
