"""
Documentation: http://docs.sonarqube.org/display/PLUG/Generic+Test+Coverage

Example:
<coverage version="1">
    <file path="src/main/java/FooBar.java">
        <lineToCover lineNumber="4" covered="true" branchesToCover="4" coveredBranches="3"/>
        <lineToCover lineNumber="5" covered="false"/>
    </file>
    <file path="src/main/js/foo.js">
        <lineToCover lineNumber="2" covered="true" branchesToCover="2" coveredBranches="1"/>
        <lineToCover lineNumber="3" covered="false"/>
        <lineToCover lineNumber="5" covered="true"/>
    </file>
</coverage>

"""
from collections import defaultdict

if __name__ =='__main__':

    result = defaultdict(list)

    result = []
    with open('coverage.out') as inp:
        for i in inp:
            line = i.strip()
            if line == 'mode: set':
                continue
            filename, tail = line.split(':')
            start_line, tail = tail.split(',', 1)
            end_line, tail = tail.split(' ', 1)
            statements, count = tail.split(' ', 1)
            start_line = int(start_line.split('.')[0])
            end_line = int(end_line.split('.')[0])
            covered = bool(int(count))
            result.append((filename, start_line, end_line, covered))

    coverage = defaultdict(list)
    for filename, start, stop, cover in result:
        for l in range(start, stop+1):
            line = '    <lineToCover lineNumber="%i" covered="%s"/>' % (l, str(cover).lower())
            coverage[filename].append(line)

    tree = ''
    for filename, lines in coverage.items():
        sub_tree = '  <file path="%s">\n' % filename
        sub_tree += '\n'.join(lines) + '\n'
        sub_tree += '  </file>\n'
        tree += sub_tree

    with open('coverage.xml', 'w') as out:
         out.write('<coverage version="1">\n'+tree+'</coverage>')
