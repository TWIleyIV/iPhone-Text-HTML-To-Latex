import re
import io
import chardet
import codecs

f = open("example.tex", "w", encoding='ISO-8859-1')

with codecs.open("fullTexts.html", "r", encoding='ISO-8859-1') as sample:
	content = sample.readlines()

prev = 'none'
printPrev = 'none'
lineSplit = ''
stillSplit = 'false'
pictureComing = 'false'

f.write('\documentclass[8pt]{extarticle}' + '\n')
f.write('\\usepackage{enumitem}' + '\n')
f.write('\\usepackage{coloremoji}' + '\n')
f.write('\\usepackage[margin=1in]{geometry}' + '\n')

f.write('\\newcommand*{\MyLabel}{}%' + '\n')
f.write('\\newenvironment{MyDescription}[2][]{%' + '\n')
f.write('\edef\MyLabel{#1}%' + '\n')
f.write('\\begin{description}[labelwidth=3.0cm, leftmargin=3.0cm, labelsep=0.0ex, font=\\normalfont]' + '\n')
f.write('\item [#2:]' + '\n')
f.write('}{%' + '\n')
f.write('    \hfill\MyLabel%' + '\n')
f.write('    \end{description}%' + '\n')
f.write('}' + '\n')

f.write('\\begin{document}' + '\n')
i = 0

myName = "Wesley"
otherName = "Teddi"
otherFullName = "Teddi Pinson"

for line in content:
	if '<span class="date">' in line:
		m = re.search('<span class="date">(.+?)</span><br />', line).group(1)
		f.write('\\noindent\makebox[\linewidth]{\\rule{\paperwidth}{0.4pt}} \\\\ \\textbf{' + str(m) + '}\n')
		prev = 'none'
		printPrev = 'none'
	elif '<span style="color:rgb(210,0,0);"><span class="senderName">Me</span>' in line:
		s = line.split('</span>')
		if s[4].strip() == '<br />':
			pictureComing = 'true'
			prev = 'me'
		elif s[4].strip().endswith('<br />'):
			splits = s[4].split('<br />')
			if prev == 'me':
				f.write('\\begin{MyDescription}{' + myName + '}' + splits[0].strip() + '\\\\\n\end{MyDescription}\n')
			else:
				f.write('\\begin{MyDescription}{' + myName + '}' + splits[0].strip() + '\\\\\n\end{MyDescription}\n')
			printPrev = 'me'
		else:
			lineSplit += s[4].strip()
			stillSplit = 'true'
		prev = 'me'
	elif '<span style="color:rgb(0,0,210);"><span class="senderName">' + otherFullName + '</span>' in line:
		s = line.split('</span>')
		if s[4].strip() == '<br />':
			pictureComing = 'true'
			prev = otherName
		elif s[4].strip().endswith('<br />'):
			splits = s[4].split('<br />')
			if prev == otherName:
				f.write('\\begin{MyDescription}{' + otherName + '}' + splits[0].strip() + '\\\\\n\end{MyDescription}\n')
			else:
				f.write('\\begin{MyDescription}{' + otherName + '}' + splits[0].strip() + '\\\\\n\end{MyDescription}\n')
			printPrev = otherName
		else:
			lineSplit += s[4].strip()
			stillSplit = 'true'
		prev = otherName
	elif stillSplit == 'true':
		if line.strip().endswith('<br />'):
			splits = line.split('<br />')
			lineSplit += ('\\\\' + splits[0].strip())
			if printPrev == otherName:
				if prev == otherName:
					f.write('\\begin{MyDescription}{' + otherName + '}' + lineSplit + '\\\\\n\end{MyDescription}\n')
				else:
					f.write('\\begin{MyDescription}{' + myName + '}' + lineSplit + '\\\\\n\end{MyDescription}\n')
			elif printPrev == 'me':
				if prev == 'me':
					f.write('\\begin{MyDescription}{' + myName + '}' + lineSplit + '\\\\\n\end{MyDescription}\n')
				else:
					f.write('\\begin{MyDescription}{' + otherName + '}' + lineSplit + '\\\\\n\end{MyDescription}\n')
			else:
				if prev == 'me':
					f.write('\\begin{MyDescription}{' + myName + '}' + lineSplit + '\\\\\n\end{MyDescription}\n')
				else:
					f.write('\\begin{MyDescription}{' + otherName + '}' + lineSplit + '\\\\\n\end{MyDescription}\n')
			stillSplit = 'false'
			lineSplit = ''
		elif "</p>" in line:
			if printPrev == otherName:
				if prev == otherName:
					f.write('\\begin{MyDescription}{' + otherName + '}' + lineSplit + '\\\\\n\end{MyDescription}\n')
				else:
					f.write('\\begin{MyDescription}{' + myName + '}' + lineSplit + '\\\\\n\end{MyDescription}\n')
			elif printPrev == 'me':
				if prev == 'me':
					f.write('\\begin{MyDescription}{' + myName + '}' + lineSplit + '\\\\\n\end{MyDescription}\n')
				else:
					f.write('\\begin{MyDescription}{' + otherName + '}' + lineSplit + '\\\\\n\end{MyDescription}\n')
			stillSplit = 'false'
			lineSplit = ''
			prev = 'none'
			printPrev = 'none'
		else:
			lineSplit += (line.strip() + '\\\\')
	elif (line.startswith('<a href="')) and line.strip() != '<br />':
		splits = line.split('<a href="')
		try:
			s = splits[1].split('" target="_blank">')
		except IndexError:
			print(i)
			print(line)
		imgSplit = s[0].split('\\')
		if prev == otherName:
			f.write('\\begin{MyDescription}{' + otherName + '}\includegraphics[scale=0.1]{' + imgSplit[0] + '/' + imgSplit[1] + '}\\\\\n\end{MyDescription}\n')
		else:
			f.write('\\begin{MyDescription}{' + myName + '}\includegraphics[scale=0.1]{' + imgSplit[0] + '/' + imgSplit[1] + '}\\\\\n\end{MyDescription}\n')
		pictureComing = 'false'
	i += 1	
f.write('\end{document}' + '\n')
		
f.close()