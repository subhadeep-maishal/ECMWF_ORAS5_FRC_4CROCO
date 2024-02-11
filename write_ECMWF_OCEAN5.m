function write_ECMWF_OCEAN5(OGCM_dir,OGCM_prefix,raw_ECMWF_OCEAN5_name,...
                         ECMWF_OCEAN5_type,vars,time,thedatemonth,Yorig)
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% 
%  Further Information:  
%  http://www.croco-ocean.org
%  
%  This file is part of CROCOTOOLS
%
%  CROCOTOOLS is free software; you can redistribute it and/or modify
%  it under the terms of the GNU General Public License as published
%  by the Free Software Foundation; either version 2 of the License,
%  or (at your option) any later version.
%
%  CROCOTOOLS is distributed in the hope that it will be useful, but
%  WITHOUT ANY WARRANTY; without even the implied warranty of
%  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
%  GNU General Public License for more details.
%
% developed by Subhadeep Maishal
% Indian Institute of Technology, Kharagpur
% subhadeepmaishal@kgpian.iitkgp.ac.in
%
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
disp(['    writing ECMWF_OCEAN5 file'])
%
% Get grid and time frame
%
nc = netcdf(raw_ECMWF_OCEAN5_name);
if mercator_type==1,
  lon = nc{'longitude'}(:);
  lat = nc{'latitude'}(:);
  depth = nc{'depth'}(:);
  time = nc{'time'}(:);
  time = time / 24 + datenum(1950,1,1) - datenum(Yorig,1,1);
end
%
% Get SSH
%
%missval = -32767;
disp('    ...SSH')
vname=sprintf('%s',vars{1});
ncc=nc{vname};
ssh=ncc(:);
missval=ncc.FillValue_(:);
scale_factor=ncc.scale_factor(:);
add_offset=ncc.add_offset(:);
ssh(ssh<=missval)=NaN;
ssh = ssh.*scale_factor + add_offset;
%
%
% Get U
%
disp('    ...U')
vname=sprintf('%s',vars{2});
ncc=nc{vname};
u=ncc(:);
missval=ncc.FillValue_(:);
scale_factor=ncc.scale_factor(:);
add_offset=ncc.add_offset(:);
u(u<=missval)=NaN;
u = u.*scale_factor + add_offset;
%
% Get V
%
disp('    ...V')
vname=sprintf('%s',vars{3});
ncc=nc{vname};
v=ncc(:);
missval=ncc.FillValue_(:);
scale_factor=ncc.scale_factor(:);
add_offset=ncc.add_offset(:);
v(v<=missval)=NaN;
v = v.*scale_factor + add_offset;
%
% Get TEMP
%
disp('    ...TEMP')
vname=sprintf('%s',vars{4});
ncc=nc{vname};
temp=ncc(:);
missval=ncc.FillValue_(:);
scale_factor=ncc.scale_factor(:);
add_offset=ncc.add_offset(:);
ktoc=272.15;
temp(temp<=missval)=NaN;
temp = temp.*scale_factor + add_offset; % - ktoc;
%
% Get SALT
%
disp('    ...SALT')
vname=sprintf('%s',vars{5});
ncc=nc{vname};
salt=ncc(:);
missval=ncc.FillValue_(:);
scale_factor=ncc.scale_factor(:);
add_offset=ncc.add_offset(:);
salt(salt<=missval)=NaN;
salt = salt.*scale_factor + add_offset;
%
% Create the ECMWF_OCEAN5 file
%
close(nc) % close raw_mercator_name

create_OGCM([OGCM_dir,OGCM_prefix,thedatemonth,'.cdf'],...
             lon,lat,lon,lat,lon,lat,depth,time,...
             squeeze(temp),squeeze(salt),squeeze(u),...
             squeeze(v),squeeze(ssh),Yorig)
%
return

end


