from lxml import etree as et

def labelXML(xmlParams):
    root = et.Element('annotation',{'verified':'yes'})
    folder = textSubElement(root, 'folder', xmlParams['folder'])
    filename = textSubElement(root, 'filename', xmlParams['filename'])
    path = textSubElement(root, 'path', xmlParams['path'])
    source = et.SubElement(root, 'source')
    database = textSubElement(source, 'database', 'Unknown')
    size = et.SubElement(root, 'size')
    width = textSubElement(size, 'width', xmlParams['width'])
    height = textSubElement(size, 'height', xmlParams['height'])
    depth = textSubElement(size, 'depth','3')
    segmented = textSubElement(root, 'segmented','0')
    object = et.SubElement(root, 'object')
    name = textSubElement(object, 'name', xmlParams['color'])
    pose = textSubElement(object, 'pose', 'Unspecified')
    truncated = textSubElement(object, 'truncated', '0')
    difficult = textSubElement(object, 'difficult', '0')
    bndbox = et.SubElement(object, 'bndbox')
    xmin = textSubElement(bndbox, 'xmin', xmlParams['xmin'])
    ymin = textSubElement(bndbox, 'ymin', xmlParams['ymin'])
    xmax = textSubElement(bndbox, 'xmax', xmlParams['xmax'])
    ymax = textSubElement(bndbox, 'ymax', xmlParams['ymax'])
    return root

def textElement(tag, text, *args, **kwargs):
    element = et.Element(tag, *args, **kwargs)
    element.text = text
    return element

def textSubElement(parent, tag, text, *args, **kwargs):
    element = et.SubElement(parent, tag, *args, **kwargs)
    element.text = text
    return element

def saveXML(filepath,filename,xmlParams):
    root = labelXML(xmlParams)
    file = open(filepath+filename+".xml", "wb")
    et.indent(root, space="    ")
    file.write(et.tostring(root,pretty_print=True),)
    return