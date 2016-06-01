function MultiFractalSpectrum(data,dimension)

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
   
   %�������в�ͬ�ֱ��ʵĻ���,��Ϊboxsz*boxsz��С����������probmlevels���ڲ�ͬ�ֱ����´洢�ĸ���С�������ܸ���
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
   
   %�������ط����ף�alpha(q)��f(q)��qranΪq�ķ�Χ��qresΪq�ķֱ���
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
   %���ƶ��ط����׵�ͼ
   figure;plot(qq,alphaqss,'r:o',qq,fqss,'g:o');
   h = legend('alpha(q)','f(q)','Location','NorthEast'); 
   xlabel('q','FontSize',14);
   figure;plot(alphaqss,fqss,'r:o');
   xlabel('alpha(q)','FontSize',14);
   ylabel('f(q)','FontSize',14);
end