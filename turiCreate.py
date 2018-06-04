#importing turi create and naming it tc for easier use later
import turicreate as tc
#loading the images into turicreate
data = tc.image_analysis.load_images(
    #the path for your image folder (change it to your own path)
    '/Users/kartikar/Desktop/image3',
    with_path=True
)

#applying labels to our image (telling turicreate what image showld be labelled as what)
data['label'] = data['path'].apply(
    #labelling the image as a cat if the folder name is cat, labelling it as a dog if it isn't
    lambda path: 'cat' if '/cat/' in path else 'dog'
)

#counting the number of each label (how many cats and dog images there are)
data.groupby('label', [tc.aggregate.COUNT])

#Dividing the images randomly in 2 sections with a ratio of 8:2
#This is important for us to check the accuracy of our model
training_data, testing_data = data.random_split(0.80)

#Training the model
model = tc.image_classifier.create(
    training_data,
    target='label',
    #using the squeezenet model for mobiles, for more accurate results use resnet-50
    model='squeezenet_v1.1',
    #number of times turicreate should attempt to train the model
    max_iterations=3000
)

#used to check the accuracy of our trained model using the images we had set aside
model.evaluate(testing_data)

#exporting the model to be used as a mlmodel used by ios
model.export_coreml('catDog.mlmodel')
