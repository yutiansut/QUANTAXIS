function MultiFractalSpectrum(data,dimension)
%原始数据可以是1维或者2维
%如果是2维,矩形区域,取最大的边为尺度,划分出一个正方形,作为场
   if dimension==2
       sizes=size(data);
       maxsz=max(sizes);
       %maxsz=min(sizes);
       field=zeros(maxsz,maxsz);
       field(1:sizes(1),1:sizes(2))=data;
   else
       field=data;
       maxsz=length(data);
   end
   
   maxboxsz=floor(log(maxsz)/log(2));
   massinmlevels={};
   probmlevels={};
   layer=4;
   
   %将场进行不同分辨率的划分,成为boxsz*boxsz的小区域，最后probmlevels是在不同分辨率下存储的各个小区域的总概率
   for layer=1:maxboxsz
       boxsz=2.^layer;
       coordinates=0:boxsz:maxsz-boxsz;
       if dimension==2
           [xx,yy]=meshgrid(coordinates);
           clusters=arrayfun(@(x,y){y+1:min(y+boxsz,maxsz),x+1:min(x+boxsz,maxsz)},yy,xx,'uniformoutput',false);
           clusters=clusters(:);
           bool=cell2mat(cellfun(@(x)(length(x{1})>0&length(x{2}>0)),clusters,'uniformoutput',false));
            clusters=clusters(bool);
           totalfields=cellfun(@(x)sum(sum(field(x{1},x{2}))),clusters,'uniformoutput',false);
           totalfields=cell2mat(totalfields);
       else
           clusters=arrayfun(@(x)x+1:min(x+boxsz,maxsz),coordinates,'uniformoutput',false);
           bool=cell2mat(cellfun(@(x)(length(x)>0),clusters,'uniformoutput',false));
           totalfields=cellfun(@(x)sum(field(x)),clusters,'uniformoutput',false);
           totalfields=cell2mat(totalfields);
       end
       massinmlevels={massinmlevels{:},totalfields};
       probmlevels={probmlevels{:},totalfields./sum(totalfields)};
   end
   
   %计算多重分形谱，alpha(q)和f(q)，qran为q的范围，qres为q的分辨率
   qran=10;qres=0.1;
   qq=-qran:qres:qran;
   fqss=[];
   alphaqss=[];
   q=-10+0.1;
   for q=qq
       fqs=[];
       alphaqs=[];
       for layer=1:maxboxsz
           bools=probmlevels{layer}>0;
           qmass=(probmlevels{layer}(bools)).^q;
           normalized=qmass./sum(qmass(~isinf(qmass)));
           fq=sum(normalized.*log(normalized));
           alphaq=sum(normalized.*log(probmlevels{layer}(bools)));
           fqs=[fqs,fq];
           alphaqs=[alphaqs,alphaq];
       end
       line1=polyfit(log(2.^(1:maxboxsz)),alphaqs,1);
       line2=polyfit(log(2.^(1:maxboxsz)),fqs,1);
       alphaqss=[alphaqss,line1(1)];
       fqss=[fqss,line2(1)];
   end
   %绘制多重分形谱的图
   figure;plot(qq,alphaqss,'r:o',qq,fqss,'g:o');
   h = legend('alpha(q)','f(q)','Location','NorthEast'); 
   xlabel('q','FontSize',14);
   figure;plot(alphaqss,fqss,'r:o');
   xlabel('alpha(q)','FontSize',14);
   ylabel('f(q)','FontSize',14);
end