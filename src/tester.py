import re
if __name__ == '__main__':
    test = """private void GenAutoNormal
      (
        int[] Vertices
          /* assume length at least 3 and coplanar if > 3, replaced with final generated vertices */
      )
      {
        if (!AutoNormals)
          {
            throw new RuntimeException("GeomBuilder.GenAutoNormal shouldn’t be called if not AutoNormals");
          } /*if*/
        final Vec3f
            V1 = TempPoints.get(Vertices[0]),
            V2 = TempPoints.get(Vertices[1]),
            V3 = TempPoints.get(Vertices[2]);
        final Vec3f FaceNormal = (V2.sub(V1)).cross(V3.sub(V2)).unit();
        final int[] NewVertices = new int[Vertices.length];
        for (int i = 0; i < Vertices.length; ++i)
          {
            NewVertices[i] = AddActual(Vertices[i], FaceNormal);
          } /*for*/
        System.arraycopy(NewVertices, 0, Vertices, 0, Vertices.length);
      } /*GenAutoNormal*/

    """
    print(re.search("^(.+)\n\(", test))