addpath(genpath('seunglab'));
rot = '../testData';
splits = dir(rot);
a = {};
for l=3:length(splits)
    if(splits(l).isdir)
        a = [a [rot '/' splits(l).name]];
        description = fileread([rot '/' splits(l).name '/description.txt']);
    end
end
dims = get_dimensions(a);
tic
evaluate_predictions(a, dims, description, rot)
toc
