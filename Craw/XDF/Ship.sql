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
    caption text,
    passage text,
    prompt  text,
    choices text array,
    answers text array,
    examid  integer,
    pid     integer,
    num     integer
);

create table tpo.xdf_portable.listening_conversation
(
    caption             text,
    prompt              text,
    local_mp3_prompt    text,
    local_mp3_listening text,
    transcription       text,
    choices             text array,
    answers             text array,
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
select caption_clean, passage_clean, audio_local_name, transcription, examid
from tpo.xdf.speaking_q2;

insert into tpo.xdf_portable.speaking_q3 (caption, passage, local_mp3, transcription, examid)
select caption_clean, passage_clean, audio_local_name, transcription, examid
from tpo.xdf.speaking_q3;

insert into tpo.xdf_portable.speaking_q4 (caption, local_mp3, transcription, examid)
select caption_clean, audio_local_name, transcription, examid
from tpo.xdf.speaking_q4;

insert into tpo.xdf_portable.writing_independent (caption, prompt, examid)
select caption_clean, passage_clean, examid
from tpo.xdf.writing_independent
WHERE trash = false;

insert into tpo.xdf_portable.writing_integrated (caption, passage, local_mp3, transcription, examid)
select caption_clean, passage_clean, audio_local_name, transcription, examid
from tpo.xdf.writing_integrated;

insert into tpo.xdf_portable.reading (caption, passage, prompt, choices, answers, examid, pid, num)
select caption_clean,
       passage_clean,
       prompt_clean,
       choices,
       answers,
       examid,
       pid,
       question_index
from tpo.xdf.reading;

insert into tpo.xdf_portable.listening_conversation (caption, prompt, local_mp3_prompt, local_mp3_listening,
                                                     transcription, choices, answers, examid, audioid, num)
select caption_clean,
       prompt_clean,
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
       prompt_clean,
       prompt_audio_local_name,
       listening_audio_local_name,
       transcription,
       choices,
       answers,
       examid,
       audioid,
       num
from tpo.xdf.listening_lecture;


-- Text array to JSON
alter table tpo.xdf_portable.reading
    alter column choices type json using array_to_json(choices);
alter table tpo.xdf_portable.reading
    alter column answers type json using array_to_json(answers);

alter table tpo.xdf_portable.listening_conversation
    alter column choices type json using array_to_json(choices);
alter table tpo.xdf_portable.listening_conversation
    alter column answers type json using array_to_json(answers);

alter table tpo.xdf_portable.listening_lecture
    alter column choices type json using array_to_json(choices);
alter table tpo.xdf_portable.listening_lecture
    alter column answers type json using array_to_json(answers);
