/*
CONNECTEDCOMPONENTS	computes the connected components of a binary graph
[comp,cmpSz] = connectedComponents(conn,nhood,sizeThreshold)
conn			a 4d 'conn' style connectivity graph
nhood			the neighborhood associated with the 'conn' graph giving the interpretation of the edges (default is the nearest neighbor 6-connectivity corresponding to 3 edges per voxel)
sizeThreshold	objects that have as many voxels or fewer than this threshold are treated as 'dust' and removed from the connected components output
comp			the output connected components labeling (sorted in descending order of size)
cmpSz			the sizes of each component
*/
#include <Python.h>
static PyObject *
spam_system(PyObject *self, PyObject *args)
{
    const char *command;
    int sts;

    if (!PyArg_ParseTuple(args, "s", &command))
        return NULL;
    sts = system(command);
    return Py_BuildValue("i", sts);
}

static PyMethodDef SpamMethods[] = {
    ...
    {"system",  spam_system, METH_VARARGS,
     "Execute a shell command."},
    ...
    {NULL, NULL, 0, NULL}        /* Sentinel */
};