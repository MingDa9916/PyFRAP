#=====================================================================================================================================
#Copyright
#=====================================================================================================================================

#Copyright (C) 2014 Alexander Blaessle, Patrick Mueller and the Friedrich Miescher Laboratory of the Max Planck Society
#This software is distributed under the terms of the GNU General Public License.

#This file is part of PyFRAP.

#PyFRAP is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.

#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.

#You should have received a copy of the GNU General Public License
#along with this program.  If not, see <http://www.gnu.org/licenses/>.

#===========================================================================================================================================================================
#Module Description
#===========================================================================================================================================================================

"""Input/Output module for PyFRAP toolbox. 

Handles saving/loading PyFRAP projects into pickled files and the memory handling that comes with it.
"""

#===========================================================================================================================================================================
#Improting necessary modules
#===========================================================================================================================================================================

import pickle
import platform
import gc
import sys
import os

from pyfrp.modules import pyfrp_misc_module

#===========================================================================================================================================================================
#Module Functions
#===========================================================================================================================================================================

def saveToPickle(obj,fn=None):
	
	"""Saves obj into pickled format.
	
	.. note:: If ``fn==Non``, will try to save to ``obj.name``, otherwise unnamed.pk
	
	Keyword Args:
		fn (str): Output file name.	
	
	Returns: 
		str: Output filename.
	
	"""
	
	cleanUp()
        if fn==None:
                if hasattr(obj,"name"):
                        fn=obj.name+".pk"
                else:
                        fn="unnamed"+".pk"
                
        with open(fn, 'wb') as output:
                pickle.dump(obj, output, pickle.HIGHEST_PROTOCOL)
        
        return fn

def loadFromPickle(fn):
	
	"""Loads obj from pickled format.
	
	Args:
		fn (str): Filename.	
	
	Returns: 
		str: Output filename.
	
	"""
	
	cleanUp()
	
	#Need to do append subclasses folder here. Sometimes pickle has problem finding the classes
	
	sys.path.append(pyfrp_misc_module.getSubclassesDir()+'/')

        if platform.system() in ["Darwin","Linux"]:
                filehandler=open(fn, 'r')
        elif platform.system() in ["Windows"]:
                filehandler=open(fn, 'rb')
                
        loadedFile=pickle.load(filehandler)
        
        return loadedFile

def loadMolecule(fn,update=True):
	
	"""Loads molecule object from pickle file
	and brings it up-to-date.
	
	Args:
		fn (str): Filename.	
	
	Keyword Args: 
		update (bool): Update to current version.
	
	Returns: 
		pyfrp.subclasses.pyfrp_molecule: Molecule file.
	
	"""
	
	mol=loadFromPickle(fn)
	if update:
		mol.update_version()
	return mol

def loadEmbryo(fn,update=True):
	
	"""Loads embryo object from pickle file
	and brings it up-to-date.
	
	Args:
		fn (str): Filename.	
	
	Keyword Args: 
		update (bool): Update to current version.
	
	Returns: 
		pyfrp.subclasses.pyfrp_embryo: Embryo file.
	
	"""
	
	emb=loadFromPickle(fn)
	if update:
		emb.update_version()
	return emb

def cleanUp():
	"""Calls garbage collector to clean up.
	"""
	
	gc.collect()
	return None

def copyMeshFiles(fn,fnGeo,fnMsh,debug=False):
	
	"""Copies meshfiles to new location. 
	
	If ``fn`` does not end on ``meshfiles``, will create a folder ``meshfiles`` 
	where to dump new files.
	
	Args:
		fn (str): Filepath or parent directory where to put meshfiles.
		fnGeo (str): Filepath of geo file.
		fnMsh (str): Filepath of msh file.
	
	Keyword Args: 
		debug (bool): Print out debugging messages.
	
	Returns:
		tuple: Tuple containing:
		
			* fnGeoNew (str): New geo file location.
			* fnMshNew (str): New msh file location.
			
	"""
	
	if not os.path.isdir(fn):
	
		fn=os.path.realpath(fn)
		fn=os.path.dirname(fn)
	
	if 'meshfiles'==os.path.split(fn)[-1]:
		if debug:
			print "Folder is already called meshfiles, will it as it is."
	else:
		fn=pyfrp_misc_module.slashToFn(fn)
		try:
			os.mkdir(fn+"meshfiles")
		except OSError:
			if debug:
				printWarning("Cannot create folder " + fn + ". Already exists")
			
		fn=pyfrp_misc_module.slashToFn(fn+"meshfiles")
		if debug:
			print "Created new folder " + fn + " ."
			
	if debug:
		cmdGeo="cp -v " + fnGeo + " " + fn
		cmdMsh="cp -v " + fnMsh + " " + fn
	else:
		cmdGeo="cp " + fnGeo + " " + fn
		cmdMsh="cp " + fnMsh + " " + fn
		
	os.system(cmdGeo)
	os.system(cmdMsh)
	
	fnGeoNew=fn+os.path.split(fnGeo)[-1]
	fnMshNew=fn+os.path.split(fnMsh)[-1]
	
	return fnGeoNew,fnMshNew
	
def copyAndRenameFile(fn,fnNew,debug=False):
	
	"""Copies file ``fn`` into same directory as ``fn`` and 
	renames it ``fnNew``.
	
	.. note:: If copying fails, then function will return old filename.
	
	Args:
		fn (str): Filepath of original file.
		fnNew (str): New filename.
	
	Keyword Args: 
		debug (bool): Print out debugging messages.
	
	Returns:
		str: Path to new file.
	
	"""
	
	head,tail=os.path.split(fn)
	ext=os.path.splitext(tail)[-1]
	fnNew=pyfrp_misc_module.slashToFn(head)+fnNew+ext
	
	if debug:
		ret=os.system("cp -v " + fn + " " + fnNew)
	else:
		ret=os.system("cp " + fn + " " + fnNew)
	
	if ret==0:
		return fnNew
	else:
		return fn
	
	
	
