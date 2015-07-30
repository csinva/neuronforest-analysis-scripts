function calcGrads()
    %% gradients at each step
    %{
    iterations = {'21','41'};
    n = length(iterations);
    preds = {};
    
    %load labels
    path = ['/groups/turaga/home/singhc/neuronforest-spark/mnt/predictions/smallGrads/malis/gradient1/big1a/0/split_555/'];
    load([path '000/dims.txt']);
    labels=load3D([path '000/points.raw'], dims);
    %load base predictions
    path = '/groups/turaga/home/singhc/neuronforest-spark/mnt/predictions/expa-train/predictions/partial4/test/big1a/0/split_555/';
    expa=load3D([path '000/predictions.raw'], dims);
    %load malis predictions
    for i=1:length(iterations)
        iter=iterations{i};
        path = ['/groups/turaga/home/singhc/neuronforest-spark/mnt/predictions/smallGrads/malis/gradient' iter '/big1a/0/split_555/'];
        preds1 = load3D([path '000/preds.raw'], dims);
        preds = [preds preds1];
    end
    %BrowseComponents('iiii',labels,expa,preds{1},preds{2});
    %differences
    BrowseComponents('iiii',labels,expa,preds{1}-expa,preds{2}-expa);
    
    iterations = {'21','41'};
    n = length(iterations);
    preds = {};
    
    %load labels
    path = ['/groups/turaga/home/singhc/neuronforest-spark/mnt/predictions/smallGrads/malis/gradient1/big1a/0/split_555/'];
    load([path '000/dims.txt']);
    labels=load3D([path '000/points.raw'], dims);
    %load base predictions
    path = '/groups/turaga/home/singhc/neuronforest-spark/mnt/predictions/expa-train/predictions/partial4/test/big1a/0/split_555/';
    expa=load3D([path '000/predictions.raw'], dims);
    %load malis predictions
    for i=1:length(iterations)
        iter=iterations{i};
        path = ['/groups/turaga/home/singhc/neuronforest-spark/mnt/predictions/smallGrads/malis/gradient' iter '/big1a/0/split_555/'];
        preds1 = load3D([path '000/preds.raw'], dims);
        preds = [preds preds1];
    end
    %BrowseComponents('iiii',labels,expa,preds{1},preds{2});
    %differences
    BrowseComponents('iiii',labels,expa,preds{1}-expa,preds{2}-expa);
    %}
    %% gradients at each step - 2 subvolumes
    %{
    iterations = {'20','40'};
    n = length(iterations);
    preds = {};
    %load labels
    path = ['/groups/turaga/home/singhc/mnt/predictions/smallGrads/malis/gradient1/big1a/0/split_555/'];
    load([path '000/dims.txt']);
    labels1=load3D([path '000/points.raw'], dims);
    labels2=load3D([path '001/points.raw'], dims);
    labels=horzcat(labels1,labels2);
    %load base predictions
    path = '/groups/turaga/home/singhc/mnt/predictions/expa-train/predictions/partial4/test/big1a/0/split_555/';
    expa1=load3D([path '000/predictions.raw'], dims);
    expa2=load3D([path '001/predictions.raw'], dims);
    expa=horzcat(expa1,expa2);
    %load malis predictions
    for i=1:length(iterations)
        iter=iterations{i};
        path = ['/groups/turaga/home/singhc/mnt/predictions/smallGrads/malis/gradient' iter '/big1a/0/split_555/'];
        preds1 = load3D([path '000/preds.raw'], dims);
        preds2 =  load3D([path '001/preds.raw'], dims);
        preds3=horzcat(preds1,preds2);
        preds = [preds preds3];
    end
    BrowseComponents('iiii',labels,expa,preds{1},preds{2});
    %differences
    %BrowseComponents('iiii',labels,expa,preds{1}-expa,preds{2}-expa);
    %}
    
    %% grads small avg
    %{
    p = ['/groups/turaga/home/singhc/neuronforest-spark/mnt/predictions/smallGrads2/malis/gradient1/big1a/0/split_555/'];
    load([p '000/dims.txt']);
    g=load3D_1([p '000/grads'],dims);
    BrowseComponents('i',g);
    %plot(g);
    %title('losses for maxDepth=2,learningRate=1.0,train on 2x78^3');
    %xlabel('iterations');
    %}
    %% grads small 3D
    %{
    p = ['/groups/turaga/home/singhc/neuronforest-spark/mnt/predictions/smallGrads2/malis/gradient41/big1a/0/split_555/'];
    load([p '000/dims.txt']);
    labels = load3D([p '000/points.raw'],dims);
    g=load3D([p '000/grads.raw'],dims);
        size(g)

    BrowseComponents('iiii',labels,g(:,:,:,1),g(:,:,:,2),g(:,:,:,3));
    %}
    %% grads small 3D - new
    addpath(genpath('malis/malis-turaga'));
    addpath(genpath('../neuronforest-spark/seunglab'));
    p = ['/groups/turaga/home/singhc/analysis-scripts/malis/001/'];
    load([p 'dims.txt']);
    labels = load3D([p 'pointsArr.raw'],dims);
    preds = load3D([p 'predsArr.raw'],dims);
    segs = load3D_1([p 'segArr.raw'],dims);
    losses = load3D([p 'losses.raw'],dims);
    

    affPos = min(preds,labels);
    affNeg = max(preds,labels);
    
%{
     for x=1:3
        for y=1:3
            for z=1:3
                for i=1:3
                    fprintf('%d,%d,%d,%d: %d\n',x,y,z,i,affPos(x,y,z))
                end
            end
        end
     end
    %}
% %     sum(affPos(:))
    sum(affNeg(:))
           
    [lossesPos,loss_p,classerr_p,randIndex_p] = malis_loss_mex(single(affPos), ...
    double(-eye(3)),uint16(segs),double(.3),boolean(true));
    
    randIndex_p
    [lossesNeg,loss,classerr,randIndex_n] = malis_loss_mex(single(affNeg), ...
    double(-eye(3)),uint16(segs),double(.3),boolean(false));
    randIndex_n
 
%                                               single(connEst(:,:,:,:,1)), ...
%                                                 m.params.nhood, ...
%                                                 uint16(segNeg), ...
%                                                 m.layers{m.layer_map.error}.param, ...
%                                                 false);
%     BrowseComponents('ii',lossesPos,lossesNeg);
%       BrowseComponents('iici',labels,preds,segs,lossesPos+lossesNeg);
BrowseComponents('ciii',segs,labels,preds>.5,losses(:,:,:,3));
end

function out = load3D( file, dims )
    fid = fopen(file, 'r', 'ieee-be');
    out = fread(fid, Inf, 'float');
    fclose(fid);
    %out = permute(reshape(out, [3 fliplr(dims)]), [4,1,2,3]);   
    out = permute(reshape(out, [3 fliplr(dims)]), [4,3,2,1]);   
end

function out = load3D_1( file, dims )
    fid = fopen(file, 'r', 'ieee-be');
    out = fread(fid, Inf, 'float');
    fclose(fid);
    out = permute(reshape(out, [1 fliplr(dims)]), [4,3,2,1]);
end