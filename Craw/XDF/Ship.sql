-- Clean start: delete all tables in tpo.xdf_portable


-- Create structure
create table tpo.xdf_portable.speaking_q1
(
    caption text,
    prompt  text,
    examid  integer
);

create table tpo.xdf_portable.speaking_q2
(
    caption       text,
    passage       text,
    local_mp3     text,
    transcription text,
    examid        integer
);

create table tpo.xdf_portable.speaking_q3 as
select *
from tpo.xdf_portable.speaking_q2
    with no data;

create table tpo.xdf_portable.speaking_q4
(
    caption       text,
    local_mp3     text,
    transcription text,
    examid        integer
);

create table tpo.xdf_portable.writing_independent as
select *
from tpo.xdf_portable.speaking_q1
    with no data;

create table tpo.xdf_portable.writing_integrated as
select *
from tpo.xdf_portable.speaking_q2
    with no data;

create table tpo.xdf_portable.reading
(
    caption   text,
    passage   text,
    prompt    text,
    paragraph integer,
    choices   text,
    answers   text,
    examid    integer,
    pid       integer,
    num       integer
);

create table tpo.xdf_portable.listening_conversation
(
    caption             text,
    prompt              text,
    local_mp3_prompt    text,
    local_mp3_listening text,
    transcription       text,
    choices text,
    answers text,
    examid              integer,
    audioid             integer,
    num                 integer
);

create table tpo.xdf_portable.listening_lecture as
select *
from tpo.xdf_portable.listening_conversation
    with no data;

-- Insert data
insert into tpo.xdf_portable.speaking_q1 (caption, prompt, examid)
select caption_clean, prompt_clean, examid
from tpo.xdf.speaking_q1;

insert into tpo.xdf_portable.speaking_q2 (caption, passage, local_mp3, transcription, examid)
select caption_clean, passage_json, audio_local_name, transcription, examid
from tpo.xdf.speaking_q2;

insert into tpo.xdf_portable.speaking_q3 (caption, passage, local_mp3, transcription, examid)
select caption_clean, passage_json, audio_local_name, transcription, examid
from tpo.xdf.speaking_q3;

insert into tpo.xdf_portable.speaking_q4 (caption, local_mp3, transcription, examid)
select caption_clean, audio_local_name, transcription, examid
from tpo.xdf.speaking_q4;

insert into tpo.xdf_portable.writing_independent (caption, prompt, examid)
select caption_clean, passage_json, examid
from tpo.xdf.writing_independent
WHERE trash = false;

insert into tpo.xdf_portable.writing_integrated (caption, passage, local_mp3, transcription, examid)
select caption_clean, passage_json, audio_local_name, transcription, examid
from tpo.xdf.writing_integrated;

insert into tpo.xdf_portable.reading (caption, passage, prompt, paragraph, choices, answers, examid, pid, num)
select caption_clean,
       passage_json,
       prompt_json,
       paragraph_num,
       choices_json,
       answers,
       examid,
       pid,
       question_index
from tpo.xdf.reading;

insert into tpo.xdf_portable.listening_conversation (caption, prompt, local_mp3_prompt, local_mp3_listening,
                                                     transcription, choices, answers, examid, audioid, num)
select caption_clean,
       prompt_text,
       prompt_audio_local_name,
       listening_audio_local_name,
       transcription,
       choices,
       answers,
       examid,
       audioid,
       num
from tpo.xdf.listening_conversation;

insert into tpo.xdf_portable.listening_lecture (caption, prompt, local_mp3_prompt, local_mp3_listening,
                                                transcription, choices, answers, examid, audioid, num)
select caption_clean,
       prompt_text,
       prompt_audio_local_name,
       listening_audio_local_name,
       transcription,
       choices,
       answers,
       examid,
       audioid,
       num
from tpo.xdf.listening_lecture;


-- text -> text[] -> JSON -> text
alter table tpo.xdf_portable.reading
    alter column answers type text using (array_to_json(answers::text[]))::text;

alter table tpo.xdf_portable.listening_conversation
    alter column choices type text using (array_to_json(choices::text[]))::text;
alter table tpo.xdf_portable.listening_conversation
    alter column answers type text using (array_to_json(answers::text[]))::text;

alter table tpo.xdf_portable.listening_lecture
    alter column choices type text using (array_to_json(choices::text[]))::text;
alter table tpo.xdf_portable.listening_lecture
    alter column answers type text using (array_to_json(answers::text[]))::text;