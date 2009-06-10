from schema.connection import *
metadata.bind.echo = True

bad_transcripts = ['ACHE', 'TRANSCRIPT1']

for tr in RefSeqTranscript.query.filter(RefSeqTranscript.transcript_id.in_(bad_transcripts)).all()
    RefSeqTranscript.delete(tr)
