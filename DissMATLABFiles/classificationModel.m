clear all;
close all;
colormap prism

% Defining Constants
datapoints = 300;
transformation = [1:1:17, zeros(1,17); zeros(1,17), 1:1:17];

% Load Classification Data
load("ionosphere_data_transformed.mat");

% Extract Features
classification_x_train=full(ionosphere_data(1:datapoints,1:34));

% Extract Labels
classification_y_train=ionosphere_data(1:datapoints,35);

% Train the Model
Mdl = fitcsvm(classification_x_train,classification_y_train, 'KernelFunction','linear', 'BoxConstraint',1);

% Transforming 34 dimentional points to 2 dimensions for plotting
transformed = zeros(2,datapoints,'double');
for i = 1:datapoints
    transformed(:,i) = transformation*classification_x_train(i,:)';
end

% Transforming 34 dimentional support vectors to 2 dimensions for plotting
sv = Mdl.SupportVectors;
transformedSV = zeros(2,size(sv,1),'double');
for i = 1:size(sv,1)
    transformedSV(:,i) = transformation*sv(i,:)';
end

% Plotting points and circling support vectors 
gscatter(transformed(1,:), transformed(2,:),classification_y_train)
hold on
plot(transformedSV(1,:),transformedSV(2,:),'ko','MarkerSize',10)
title("SVM Visualised")
legend('Bad radar returns','Good radar returns','Support Vectors')
hold off

% Extract Testing Set
classification_x_test=full(ionosphere_data(datapoints+1:end,1:34));
classification_y_test=ionosphere_data(datapoints+1:end,35);

% Test Model against Test Data
predictedLabels = predict(Mdl,classification_x_test);

% Compare Actual Test Labels with Predicted Labels
comparisionMatrix = not(xor(predictedLabels,classification_y_test));
accuracy=(sum(comparisionMatrix) / size(comparisionMatrix,1)) * 100