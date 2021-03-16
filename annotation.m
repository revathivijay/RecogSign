%% initialise matlab
clc
clear
close all;
warning('off')

pad = 30; % padding around the circle detected ensureing the full signs is enclosed

class = '8';

target = 'C:\Users\aadiv\Documents\VJTI\RecogSign\Train\';
target = strcat(target,class,'\');

destination = strcat(target,'Resized\');


%% basic folder check
if ~isfolder(target)
  errorMessage = sprintf('Error: The following folder does not exist:\n%s', target);
  uiwait(warndlg(errorMessage));
  return;
else
    disp("success");
end


filePattern = fullfile(target, '*.png'); %read all png files in target
jpegFiles = dir(filePattern);
baseFileName = string(zeros(length(jpegFiles),1)); %convert names to string

for k = 1:length(jpegFiles)
  temp = convertCharsToStrings(jpegFiles(k).name);
  baseFileName(k,1) = temp;
end

%% initialise final matrix 
mat = strings([length(baseFileName),8]); 
mat(1,:) = [ "filename", "xmax", "ymax", "xmin", "ymin", "class", "width", "height" ];
% mat = [];
k = 0;


ha = waitbar(0,'Please wait...');


%% heres where the magic happens

for i=1:length(baseFileName)
%     uncomment if figure is needded, uncomment all sublpots as well
%     f = figure(1); 
%     set(f,'Position',[100 100 1000 500])

    img = imread(strcat(target,baseFileName(i)));
    [height,width,d] = size(img);
    img = imresize(img,[224,224]);
    
    rgbImg = img;
    img = rgb2gray(img);
        
    og = img;
    img = edge(img,'canny'); %edge detection using canny to locate circles
%     img = bwareaopen(img,100);
    
    [centers, radii] = imfindcircles(img, [30 1000]); %detect circles, radii = [30,1000]
    
    
%     subplot(1,2,1)
%     axis on;
%     imshow(rgbImg);hold on;
%     viscircles(centers, radii,'EdgeColor','b');
    
    
    if(isempty(centers)) % no circles detected in Canny

        [centersIn, radiiIn] = imfindcircles(rgbImg, [30 1000],...
            'ObjectPolarity','dark','Sensitivity',0.95,'Method','twostage');
        
        if(~isempty(centersIn)) % circles detected in OG RGB image
%             subplot(1,2,1)
%             viscircles(centersIn(1,:), radiiIn(1),'EdgeColor','b');
            x = centersIn(1,1)-radiiIn(1)-pad;
            y = centersIn(1,2)-radiiIn(1)-pad;
            w = 2*(radiiIn(1)+pad);
            h = 2*(radiiIn(1)+pad);
%             subplot(1,2,2)
%             axis on;
%             imshow(rgbImg);hold on;
%             rectangle('Position', [x,y,w,h],'EdgeColor','b', 'LineWidth', 3);
            mat(i+1,:) = [string(baseFileName(i)),int2str(x+w),int2str(y+h),...
                int2str(x),int2str(y),class,int2str(width),int2str(height)];
        end
                
    else % if a circle is detected in canny, use it to draw BBox

        x = centers(1,1)-radii(1)-pad;
        y = centers(1,2)-radii(1)-pad;
        w = 2*(radii(1)+pad);
        h = 2*(radii(1)+pad);
        
%         subplot(1,2,2)
%         axis on;
%         imshow(rgbImg);hold on;
%         rectangle('Position', [x,y,w,h],'EdgeColor','y', 'LineWidth', 3);

        mat(i+1,:) = [string(baseFileName(i)),int2str(x+w),int2str(y+h),...
            int2str(x),int2str(y),class,int2str(width),int2str(height)];

    end
    dest = strcat(destination,baseFileName(i));
    imwrite(rgbImg,dest);
%     hold off
%     pause(1)
    waitbar(i/length(baseFileName),ha);
end
disp(k)
delete(ha);
writematrix(mat,strcat(target,'annotClass',class,'.csv')); %write matrix into a csv file

load gong.mat; 
soundsc(y);