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
static PyObject * hello_wrapper(PyObject * self, PyObject * args)
{
  char * input;
  char * result;
  PyObject * ret;

  // parse arguments
  if (!PyArg_ParseTuple(args, "s", &input)) {
    return NULL;
  }

  // run the actual function
  result = hello(input);

  // build the resulting string into a Python object.
  ret = PyString_FromString(result);
  free(result);

  return ret;
}

static PyMethodDef HelloMethods[] = {
 { "hello", hello_wrapper, METH_VARARGS, "Say hello" },
 { NULL, NULL, 0, NULL }
};

DL_EXPORT(void) inithello(void)
{
  Py_InitModule("hello", HelloMethods);
}
