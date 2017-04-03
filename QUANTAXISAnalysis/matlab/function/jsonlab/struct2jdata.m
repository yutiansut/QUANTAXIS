function newdata=struct2jdata(data,varargin)
%
% newdata=struct2jdata(data,opt,...)
%
% convert a JData object (in the form of a struct array) into an array
%
% authors:Qianqian Fang (fangq<at> nmr.mgh.harvard.edu)
%
% input:
%      data: a struct array. If data contains JData keywords in the first
%            level children, these fields are parsed and regrouped into a
%            data object (arrays, trees, graphs etc) based on JData 
%            specification. The JData keywords are
%               "_ArrayType_", "_ArraySize_", "_ArrayData_"
%               "_ArrayIsSparse_", "_ArrayIsComplex_"
%      opt: (optional) a list of 'Param',value pairs for additional options 
%           The supported options include
%               'Recursive', if set to 1, will apply the conversion to 
%                            every child; 0 to disable
%
% output:
%      newdata: the covnerted data if the input data does contain a JData 
%               structure; otherwise, the same as the input.
%
% examples:
%      obj=struct('_ArrayType_','double','_ArraySize_',[2 3],
%                 '_ArrayIsSparse_',1 ,'_ArrayData_',null);
%      ubjdata=struct2jdata(obj);
%
% license:
%     BSD License, see LICENSE_BSD.txt files for details 
%
% -- this function is part of JSONLab toolbox (http://iso2mesh.sf.net/cgi-bin/index.cgi?jsonlab)
%

fn=fieldnames(data);
newdata=data;
len=length(data);
if(jsonopt('Recursive',0,varargin{:})==1)
  for i=1:length(fn) % depth-first
    for j=1:len
        if(isstruct(getfield(data(j),fn{i})))
            newdata(j)=setfield(newdata(j),fn{i},jstruct2array(getfield(data(j),fn{i})));
        end
    end
  end
end
if(~isempty(strmatch('x0x5F_ArrayType_',fn)) && ~isempty(strmatch('x0x5F_ArrayData_',fn)))
  newdata=cell(len,1);
  for j=1:len
    ndata=cast(data(j).x0x5F_ArrayData_,data(j).x0x5F_ArrayType_);
    iscpx=0;
    if(~isempty(strmatch('x0x5F_ArrayIsComplex_',fn)))
        if(data(j).x0x5F_ArrayIsComplex_)
           iscpx=1;
        end
    end
    if(~isempty(strmatch('x0x5F_ArrayIsSparse_',fn)))
        if(data(j).x0x5F_ArrayIsSparse_)
            if(~isempty(strmatch('x0x5F_ArraySize_',fn)))
                dim=double(data(j).x0x5F_ArraySize_);
                if(iscpx && size(ndata,2)==4-any(dim==1))
                    ndata(:,end-1)=complex(ndata(:,end-1),ndata(:,end));
                end
                if isempty(ndata)
                    % All-zeros sparse
                    ndata=sparse(dim(1),prod(dim(2:end)));
                elseif dim(1)==1
                    % Sparse row vector
                    ndata=sparse(1,ndata(:,1),ndata(:,2),dim(1),prod(dim(2:end)));
                elseif dim(2)==1
                    % Sparse column vector
                    ndata=sparse(ndata(:,1),1,ndata(:,2),dim(1),prod(dim(2:end)));
                else
                    % Generic sparse array.
                    ndata=sparse(ndata(:,1),ndata(:,2),ndata(:,3),dim(1),prod(dim(2:end)));
                end
            else
                if(iscpx && size(ndata,2)==4)
                    ndata(:,3)=complex(ndata(:,3),ndata(:,4));
                end
                ndata=sparse(ndata(:,1),ndata(:,2),ndata(:,3));
            end
        end
    elseif(~isempty(strmatch('x0x5F_ArraySize_',fn)))
        if(iscpx && size(ndata,2)==2)
             ndata=complex(ndata(:,1),ndata(:,2));
        end
        ndata=reshape(ndata(:),data(j).x0x5F_ArraySize_);
    end
    newdata{j}=ndata;
  end
  if(len==1)
      newdata=newdata{1};
  end
end