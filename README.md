GsConcordance
=============

Course project - simple concordance website using Django

This is a project done for a school project.

You can add text files that are later searchable for words, phrases and more.

There are a couple of SPs you need to create:

CREATE DEFINER=`root`@`localhost` PROCEDURE `SP_GET_PHRASE_BY_PHRASE_ID`(IN L_phrase_id INTEGER, IN L_file_id INTEGER)
BEGIN
	
	SELECT COUNT(*)
	INTO @L_phrase_length
	FROM `words_wordphraseword`
	WHERE `wordphrase_id` =L_phrase_id;
	
	SELECT word_id
	INTO @L_first_word_id
	FROM `words_wordphraseword`
	WHERE `wordphrase_id` = L_phrase_id
	ORDER BY sort
	LIMIT 1;
	
	SELECT	GROUP_CONCAT(w.value ORDER BY wp.`sort` SEPARATOR ' ')
	INTO	@S_phrase
	FROM 	words_word w JOIN `words_wordphraseword` wp ON w.id = wp.word_id
	WHERE 	`wordphrase_id` = L_phrase_id;
			
	SELECT DISTINCT fw.*, search_phrase AS word_value,file_title,fw.file_id,
		GROUP_CONCAT(
			CASE WHEN gfw.`wordno` BETWEEN fw.`wordno` AND fw.wordno + @L_phrase_length-1 
				THEN CONCAT('<b>',gfw.`word_original`,'</b>') 
				ELSE gfw.`word_original` END
			ORDER BY gfw.wordno SEPARATOR ' ') AS sample_text
	FROM words_word w JOIN files_fileword fw ON w.id = fw.word_id
		JOIN files_fileword gfw ON fw.file_id = gfw.file_id AND gfw.wordno BETWEEN fw.wordno-20 AND fw.wordno+20
		JOIN  (
			SELECT 	*
			FROM 	(	
				SELECT 	@L_phrase_length, @L_first_word_id,
					GROUP_CONCAT(w.value ORDER BY gfw.`wordno` SEPARATOR ' ') AS search_phrase,
					fw.id AS fileword_id, ff.title AS file_title, ff.id AS file_id
				FROM 	files_fileword fw JOIN files_fileword gfw ON fw.file_id = gfw.file_id
						AND gfw.wordno BETWEEN fw.wordno AND fw.wordno+@L_phrase_length-1
					JOIN words_word w ON gfw.word_id = w.id
					JOIN files_file ff ON fw.`file_id` = ff.id
				WHERE 	fw.word_id = @L_first_word_id AND (fw.file_id = L_file_id OR L_file_id = 0)
					AND gfw.word_id IN (SELECT word_id FROM words_wordphraseword WHERE `wordphrase_id` = L_phrase_id)
				GROUP BY fw.id
				LIMIT 100
				) tbl
			WHERE	search_phrase = @S_phrase
			) tbl_phrases ON fw.id = tbl_phrases.fileword_id
	WHERE fw.file_id = L_file_id OR L_file_id = 0
	GROUP BY fw.id;
    END$$

-----------------------------------------------------

CREATE DEFINER=`root`@`localhost` PROCEDURE `SP_GET_STATS_BY_FILE_ID`(IN L_file_id INTEGER)
BEGIN
	SELECT AVG(LENGTH(VALUE)) AS avg_wordlength, MIN(LENGTH(VALUE)) AS min_wordlength, MAX(LENGTH(VALUE)) AS max_wordlength
	INTO @avg_wordlength,  @min_wordlength, @max_wordlength
	FROM words_word
	WHERE active=TRUE AND (L_file_id IS NULL OR id IN (SELECT word_id FROM files_fileword WHERE file_id = L_file_id));
	SELECT AVG(sentence_length) AS avg_sentencelength, MIN(sentence_length) AS min_sentencelength, MAX(sentence_length) AS max_sentencelength
	INTO @avg_sentencelength,  @min_sentencelength, @max_sentencelength
	FROM (
		SELECT SUM(LENGTH(VALUE)) AS sentence_length,fw.`file_id`, fw.`sentenceno` 
		FROM words_word w JOIN files_fileword fw ON w.id = fw.`word_id`
		GROUP BY fw.`file_id`, fw.`sentenceno`
		) tbl_sentence_length
	WHERE (L_file_id IS NULL OR file_id = L_file_id);
	SELECT AVG(file_length) AS avg_filelength, MIN(file_length) AS min_filelength, MAX(file_length) AS max_filelength
	INTO @avg_filelength,  @min_filelength, @max_filelength
	FROM (
		SELECT SUM(LENGTH(VALUE)) AS file_length,fw.`file_id`, fw.`sentenceno` 
		FROM words_word w JOIN files_fileword fw ON w.id = fw.`word_id`
		GROUP BY fw.`file_id`
		) tbl_sentence_length
	WHERE (L_file_id IS NULL OR file_id = L_file_id);
	SELECT AVG(sentence_words) AS avg_sentencewords, MIN(sentence_words) AS min_sentencewords, MAX(sentence_words) AS max_sentencewords
	INTO @avg_sentencewords,  @min_sentencewords, @max_sentencewords
	FROM (
		SELECT COUNT(fw.id) AS sentence_words,fw.`file_id`, fw.`sentenceno` 
		FROM files_fileword fw 
		GROUP BY fw.`file_id`, fw.`sentenceno`
		) tbl_sentence_words
	WHERE (L_file_id IS NULL OR file_id = L_file_id);
	SELECT AVG(file_words) AS avg_filewords, MIN(file_words) AS min_filewords, MAX(file_words) AS max_filewords
	INTO @avg_filewords,  @min_filewords, @max_filewords
	FROM (
		SELECT COUNT(fw.id) AS file_words,fw.`file_id`, fw.`sentenceno` 
		FROM files_fileword fw 
		GROUP BY fw.`file_id`
		) tbl_file_words
	WHERE (L_file_id IS NULL OR file_id = L_file_id);
	
	SELECT ROUND(@avg_wordlength,2) AS avg_wordlength,  @min_wordlength AS min_wordlength, @max_wordlength AS max_wordlength
		,ROUND(@avg_sentencelength,2) AS avg_sentencelength,  @min_sentencelength AS min_sentencelength, @max_sentencelength AS max_sentencelength
		,ROUND(@avg_filelength,2) AS avg_filelength,  @min_filelength AS min_filelength, @max_filelength AS max_filelength
		,ROUND(@avg_sentencewords,2) AS avg_sentencewords,  @min_sentencewords AS min_sentencewords, @max_sentencewords AS max_sentencewords
		,ROUND(@avg_filewords,2) AS avg_filewords,  @min_filewords AS min_filewords, @max_filewords AS max_filewords;
		
    END$$

---------------------------------------------------------------------

CREATE DEFINER=`root`@`localhost` PROCEDURE `SP_GET_WORD_BY_WORD_ID`(IN L_word_id INTEGER, IN L_file_id INTEGER)
BEGIN
	SELECT fw.*, w.value AS word_value, ff.title AS file_title,
		GROUP_CONCAT(
			CASE WHEN fw.`id` = gfw.`id` 
				THEN CONCAT('<b>',gfw.`word_original`,'</b>') 
				ELSE gfw.`word_original` END
		ORDER BY gfw.wordno SEPARATOR ' ') AS sample_text
	FROM words_word w JOIN files_fileword fw ON w.id = fw.word_id
		JOIN files_fileword gfw ON fw.file_id = gfw.file_id AND gfw.wordno BETWEEN fw.wordno-20 AND fw.wordno+20
		JOIN files_file ff ON fw.`file_id` = ff.id
	WHERE w.id = L_word_id AND (fw.file_id = L_file_id OR L_file_id = 0)
	GROUP BY fw.id
	ORDER BY wordno;
    END$$

-------------------------------------------------------------------------

CREATE DEFINER=`root`@`localhost` PROCEDURE `SP_GET_WORDS_BY_FILE_ID`(IN L_file_id INTEGER)
BEGIN
	SELECT w.*, COUNT(*) AS appears
	FROM words_word w JOIN files_fileword fw ON w.id = fw.word_id
	WHERE fw.file_id = L_file_id
	GROUP BY w.id
	ORDER BY w.value;
    END$$
