%% Read In 250 Images
im = zeros(250,250,219);
counter = 1;
for i=2615:2615+219
   f = ['../flydata/t/grayscale_maps/iso.' num2str(i) '.png'];
   im(:,:,counter)=imread(f);
   counter=counter+1;
end

%% Read in 520 Images
im2 = zeros(520,520,490);
counter = 1;
for i=3505:3505+490
   f = ['../flydata/v/grayscale_maps/iso.0' num2str(i) '.png'];
   im2(:,:,counter)=imread(f);
   counter=counter+1;
end

%% Read and stitch hd5
im = hdf5read('/nobackup/turaga/data/fibsem_medulla_7col/trvol-250-2-h5/img_normalized.h5','main');
groundtruth = hdf5read('/nobackup/turaga/data/fibsem_medulla_7col/trvol-250-2-h5/groundtruth_seg.h5','main');
BrowseComponents('ii',im,single(groundtruth));

%% Stitch Raw Together
addpath(genpath('seunglab'));
for expt = {'1-tree-small'}
    dir1 = ['mnt/predictions/' expt{1} '/predictions'];
    files1 = dir(dir1);
    for i = 3:length(files1)
        partial = files1(i).name;
        dir2 = [dir1 '/' partial];
        files2 = dir(dir2);
        for j = 3:length(files2)           
            depth = files2(j).name;
            trainortest = 'test';
            dir3 = [dir2 '/' trainortest];
            files3 = dir(dir3);
                root = [dir3 '/' '0/222/small1a/0/split_333'];
                    fprintf('\nDir: %s\n', root);
                    DIM = 73;
                    counter=0;
                    labelArr = zeros(3*DIM,3*DIM,3*DIM,3);
                    predArr = zeros(3*DIM,3*DIM,3*DIM,3);
                    for x=0:0
                        for y=0:0
                            for z=0:0
                                imDir = [root '/' num2str(x) num2str(y) num2str(z) '/labels.raw'];
                                fid = fopen(imDir, 'r', 'ieee-be');
                                lab = fread(fid,Inf,'float');
                                fclose(fid);
                                labels = permute(reshape(lab, [3 DIM DIM DIM]), [2,3,4,1]);
                                
                                imDir = [root '/' num2str(x) num2str(y) num2str(z) '/predictions.raw'];
                                fid = fopen(imDir, 'r', 'ieee-be');
                                pred = fread(fid,Inf,'float');
                                fclose(fid);
                                predictions = permute(reshape(pred, [3 DIM DIM DIM]), [2,3,4,1]);
                                
                                counter = counter+1;
                                imOffset = [z*DIM, y*DIM, x*DIM];
                                disp(num2str(counter));
                                for x_=1:DIM
                                    for y_=1:DIM
                                       for z_=1:30
                                           offset=imOffset +[x_,y_,z_];
                                           labelArr(offset(1),offset(2),offset(3),:)=labels(x_,y_,z_,:);
                                           predArr(offset(1),offset(2),offset(3),:)=predictions(x_,y_,z_,:);
                                       end
                                    end
                                end
                                
                            end
                        end
                    end
                    BrowseComponents('iii',im,rot90(fliplr(labelArr)),rot90(fliplr(predArr)));
        end
    end
end

%% Overlayed Graphs
clf;
expts={'10-1','100-1','200-1','10-127','100-127',};
n = length(expts);
c=hsv(n);
r_ts=nan(n,1);
r_fs=nan(n,1);
for expt_index = 1:n
    expt=expts{expt_index};
    dir1 = ['mnt/masters_predictions/' expt '/predictions'];
    files1 = dir(dir1);
    for i = 3:length(files1)
        partial = files1(i).name;
        dir2 = [dir1 '/' partial];
        files2 = dir(dir2);
        for j = 3:length(files2)           
            depth = files2(j).name;
            dir3 = [dir2 '/' depth];
            files3 = dir(dir3);
                trainortest = 'test';
                root = [dir3 '/' trainortest];
                fprintf('\nDir: %s\n', root);
                load([root '/errors_new.mat']);
                d = load([root '/errors_new.mat']);
                subplot(2,2,1);
                plot(r_thresholds, r_fscore,'color',c(expt_index,:));
                hold on;

                subplot(2,2,2);
                r_fp_rate = r_fp/r_neg;
                [r_fp_rate, idxs] = sort(r_fp_rate);
                r_tp_rate = r_tp(idxs)/r_pos;
                while(any(diff(r_tp_rate)<=0))
                    r_fp_rate = r_fp_rate(diff([-inf r_tp_rate])>0);
                    r_tp_rate = r_tp_rate(diff([-inf r_tp_rate])>0);
                end
                plot(r_fp_rate, r_tp_rate,'color',c(expt_index,:));
                hold on;

                subplot(2,2,3);
                plot(p_thresholds, p_err,'color',c(expt_index,:));
                hold on;

                subplot(2,2,4);
                plot(p_fp/p_neg, p_tp/p_pos,'color',c(expt_index,:),'displayname',expt);
                hold on;
        end
    end
end
subplot(2,2,1);
title('Rand F-Score');
xlabel('Threshold');
ylabel('Rand F-Score');
xlim([r_thresholds(min_threshold_idx), r_thresholds(max_threshold_idx)]); %only does this based on last curve...
ylim([0, 1]);

subplot(2,2,2);
title('Rand Error ROC');
xlabel('False Positive');
ylabel('True Positive');
xlim([0, 1]);
ylim([0, 1]);

subplot(2,2,3);
title('Pixel Error');
xlabel('Threshold');
ylabel('Pixel Error');
xlim([p_thresholds(min_threshold_idx), p_thresholds(max_threshold_idx)]); %only does this based on last curve...
ylim([.03, .1]);

subplot(2,2,4);
title('Pixel Error ROC');
xlabel('False Positive');
ylabel('True Positive');
xlim([0, 1]);
ylim([.8, 1]);
legend(gca,'show');


plt = subplot(2,2,1);
saveas(plt, 'plots/nFeatures-trees-sampling-curves.pn','png');

%% Plot Bests
%expts={'10-fly-validate','100-fly-validate','100-fly-validate-1boost','100-fly-validate-1bigboost','100-fly-validate-5bigboost','100-fly-validate-10bigboost'};
fig = figure;
expts={'10-1','100-1','200-1','10-127','100-127',};
n = length(expts);
c=hsv(n);
rs=zeros(n,1);
ps=zeros(n,1);
for expt_index = 1:n
    expt=expts{expt_index};
    dir1 = ['mnt/masters_predictions/' expt '/predictions'];
    files1 = dir(dir1);
    for i = 3:length(files1)
        partial = files1(i).name;
        dir2 = [dir1 '/' partial];
        files2 = dir(dir2);
        for j = 3:length(files2)           
            depth = files2(j).name;
            dir3 = [dir2 '/' depth];
            files3 = dir(dir3);
                trainortest = 'test';
                root = [dir3 '/' trainortest];
                load([root '/errors_new.mat']);
                d = load([root '/errors_new.mat']);
                rs(expt_index)=max(r_fscore);
                ps(expt_index)=min(p_err);
        end
    end
end
%bar([ps rs]);
[hAx,hLine1,hLine2]=plotyy(1:n, rs, 1:n, ps);
%text(1:n,rs',num2str(rs,'%0.4f'),'HorizontalAlignment','center','VerticalAlignment','bottom')
set(figure(1), 'Position', [20 20 1800 1800])
set(gca,'XtickLabel',expts,'XTick',1:n);
title('Best F-Score and Pixel Error');
ylabel(hAx(1),'Max Rand F-Score');
hLine1.Marker='o';
ylabel(hAx(2),'Min Pixel Error');
hLine2.Marker='o';
saveas(fig, 'plots/nFeatures-trees-sampling-bests.png', 'png');

%% Stitch txts together
addpath(genpath('seunglab'));
for expt = {'1-tree-very-small_2'}
    dir1 = ['mnt/predictions/' expt{1} '/predictions'];
    files1 = dir(dir1);
    for i = 3:length(files1)
        partial = files1(i).name;
        dir2 = [dir1 '/' partial];
        files2 = dir(dir2);
        for j = 3:length(files2)           
            depth = files2(j).name;
            dir3 = [dir2 '/' 'test'];
            files3 = dir(dir3);
                bigorsmall = 'small1';
                root = [dir3 '/' bigorsmall];
                    fprintf('\nDir: %s\n', root);
                    DIM = 73;
                    counter=0;
                    arr = zeros(3*DIM,3*DIM,3*DIM,3);
                    arr2 = zeros(3*DIM,3*DIM,3*DIM,3);
                    for x=0:0 %This can be cranked up
                        for y=0:2
                            for z=0:2
                                imDir = [root '/0/split_333/' num2str(x) num2str(y) num2str(z) '/labels.txt'];
                                image = load(imDir);
                                labels = permute(reshape(image, [DIM DIM DIM 3]), [1,2,3,4]);
                                
                                imDir = [root '/0/split_333/' num2str(x) num2str(y) num2str(z) '/predictions.txt'];
                                image = load(imDir);
                                predictions = permute(reshape(image, [DIM DIM DIM 3]), [1,2,3,4]);

                                imOffset = [z*DIM, y*DIM, x*DIM];
                                disp(num2str(counter));
                                counter=counter+1;
                                for x_=1:DIM
                                    for y_=1:DIM
                                       for z_=1:30 %This can be cranked up also
                                           offset=imOffset +[x_,y_,z_];
                                           arr(offset(1),offset(2),offset(3),:)=labels(x_,y_,z_,:);
                                           arr2(offset(1),offset(2),offset(3),:)=predictions(x_,y_,z_,:);
                                       end
                                    end
                                end
                                
                            end
                        end
                    end
                    BrowseComponents('iii',im,rot90(fliplr(arr)),arr2);
        end
    end
end


%% Stitch PNGs Together
addpath(genpath('seunglab'));
for expt = {'10-trees-full'} %change this
    dir1 = ['mnt/predictions/' expt{1} '/predictions'];
    files1 = dir(dir1);
    for i = 3:length(files1)
        partial = files1(i).name;
        dir2 = [dir1 '/' partial];
        files2 = dir(dir2);
        %for j = 3:length(files2)           
            trainortest = 'test';%files2(j).name;
            dir3 = [dir2 '/' trainortest];
            files3 = dir(dir3);
                smallorbig = 'small1'; %and this
                root = [dir3 '/' smallorbig];
                    fprintf('\nDir: %s\n', root);
                    DIM = 73;
                    counter=0;
                    arr = zeros(3*DIM,3*DIM,3*DIM,3);
                    arr2 = zeros(3*DIM,3*DIM,3*DIM,3);
                    for x=0:2
                        for y=0:2
                            for z=0:2
                                root = 'mnt/predictions/1-tree-big_2/predictions/partial1/test/small1/0';
                                rootDir = [root '/split_333/' num2str(x) num2str(y) num2str(z) '/'];
                                labels = imread([rootDir 'labels.png']);
                                predictions = imread([rootDir 'predictions.png']);
                                counter = counter+1;
                                imOffset = [y*DIM, z*DIM, x];
                                disp(num2str(counter));
                                for x_=1:DIM
                                    for y_=1:DIM
                                       for z_=1:1
                                           offset=imOffset +[x_,y_,z_];
                                           arr(offset(1),offset(2),offset(3),:)=labels(x_,y_,z_,:);
                                           arr2(offset(1),offset(2),offset(3),:)=predictions(x_,y_,z_,:);
                                       end
                                    end
                                end
                                
                            end
                        end
                    end
                    im = zeros(250,250,4);
                    counter = 1;
                    for i=2615:DIM:2615+218
                       f = ['../flydata/t/grayscale_maps/iso.' num2str(i) '.png'];
                       im(:,:,counter)=imread(f);
                       counter=counter+1;
                    end
                    BrowseComponents('iii',im,arr,arr2);
                    
    end
end

%% Browse Components
addpath(genpath('seunglab'));
for expt = {'100-fly-validate'}
    dir1 = ['mnt/masters_predictions/' expt{1} '/predictions'];
    files1 = dir(dir1);
    for i = 3:length(files1)
        partial = files1(i).name;
        dir2 = [dir1 '/' partial];
        files2 = dir(dir2);
        for j = 3:length(files2)           
            depth = files2(j).name;
            dir3 = [dir2 '/' depth];
            files3 = dir(dir3);
                trainortest = 'test';
                root = [dir3 '/' trainortest];
                    fprintf('\nDir: %s\n', root);
                                      
                    dims = load([root '/0/dimensions.txt']);
                    [ affTrue, affEst, dimensions ] = load_affs( [root '/0'], dims );
                    BrowseComponents('ii',affTrue,affEst);
                    %openfig([root '/errors_new.fig']);
        end
    end
end
