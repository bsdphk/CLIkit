#!/usr/local/bin/python
#
# Copyright 2012 Poul-Henning Kamp <phk@FreeBSD.org> 
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE AUTHOR AND CONTRIBUTORS ``AS IS'' AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL AUTHOR OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
# OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
# HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
# OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
# SUCH DAMAGE.
#
# This is a slightly weird Python program:  It writes C-code.
#
# It can be run in two modes:
#
# With the argument "--tree" it will parse a CLI-langauge specification
# and write out a .h and .c file with code to implement that CLI structure.
#
# With the argument "--code" it will write out a .h and .c file that provides
# the infrastructure code necessary for the --tree generated code.
#
# The reason for this split is that you might have multiple invocations
# with --tree in a software project, for instance once for each loadable
# module etc.
#

from __future__ import print_function

import sys
import os

#######################################################################
#

types = {
	'REAL':	"double",
	'UINT':	"unsigned",
	'INT':	"int",
	'WORD':	"const char *",
}

#######################################################################
#

def usage(txt = None):
	if txt != None:
		sys.stderr.write("Error: " + txt + "\n")
	sys.stderr.write("""Usage:
	CLIkit.py --code [-o basename] [opts]
		Emit the CLIkit implementation to basename.[ch]

	CLIkit.py --tree foo.clikit [opts]
		Compile foo.clikit to foo.[ch]
""")
	exit(2)

#######################################################################
#

def do_copyright(fd):
	fd.write("""/*
 * Copyright 2012 Poul-Henning Kamp <phk@FreeBSD.org> 
 * All rights reserved.
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions
 * are met:
 * 1. Redistributions of source code must retain the above copyright
 *    notice, this list of conditions and the following disclaimer.
 * 2. Redistributions in binary form must reproduce the above copyright
 *    notice, this list of conditions and the following disclaimer in the
 *    documentation and/or other materials provided with the distribution.
 *
 * THIS SOFTWARE IS PROVIDED BY THE AUTHOR AND CONTRIBUTORS ``AS IS'' AND
 * ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
 * IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
 * ARE DISCLAIMED.  IN NO EVENT SHALL AUTHOR OR CONTRIBUTORS BE LIABLE
 * FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
 * DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
 * OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
 * HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
 * LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
 * OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
 * SUCH DAMAGE.
 *
 * NB: This file is generated by CLIkit.py: *** Do Not Edit By Hand ***
 */

""")

def do_code(argv):
	pfx = "clikit"
	if len(argv) > 0 and argv[0] == "-o":
		if len(argv) < 2:
			usage()
		pfx = argv[1]
		argv = argv[2:]
	print("DO_CODE", "PFX=%s" % pfx, argv)
	if len(argv) > 0:
		usage("XXX: no options supported yet")

	fo = open(pfx + ".h", "w")
	do_copyright(fo)
	fo.write("""
#ifndef __CLIKIT_H__
#define __CLIKIT_H__

struct clikit;
struct clikit_context;

typedef int clikit_match_f(struct clikit_context *);

struct clikit * CLIkit_New(void);
int CLIkit_Destroy(struct clikit *);
/* Cfk_ErrorHandling() */

int CLIkit_Add_Prefix(struct clikit *, const char *pfx, unsigned val);
int CLIkit_Del_Prefix(const struct clikit *, const char *pfx);

int CLIkit_Add_Tree(struct clikit *, clikit_match_f *func,
    const char *root);
int CLIkit_Del_Tree(const struct clikit *, clikit_match_f *func,
    const char *root);

struct clikit_context *CLIkit_New_Context(struct clikit *);
int CLIkit_Destroy_Context(struct clikit_context *);
void CLIkit_Input(struct clikit_context *, const char *);
/* output handler */
/* input handler */

#ifdef CLIKIT_INTERNAL
int clikit_int_match(struct clikit_context *, const char *);
int clikit_int_eol(struct clikit_context *);
void clikit_int_push_instance(struct clikit_context *);
void clikit_int_pop_instance(struct clikit_context *);
int clikit_int_unknown(struct clikit_context *);
""")
	for i in types:
		fo.write("int clikit_int_arg_%s" % i +
		    "(struct clikit_context *, %s*);\n" % types[i])
	fo.write("""
#endif /* CLIKIT_INTERNAL */

#endif /* __CLIKIT_H__ */
""")
	fo.close()

	fo = open(pfx + ".c", "w")
	do_copyright(fo)
	fo.write("""

/*********************************************************************/

#include <assert.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>

""")
	fo.write("#include \"%s.h\"\n" % pfx)
	fo.write("""

/* XXX: need <sys/queue.h> */
/* XXX: need "miniobj.h" */
/* XXX: need "argv.h" */
/* XXX: need "lineup.h" */

/********************************************************************
 * From FreeBSD's <sys/queue.h>
 * Copyright (c) 1991, 1993
 *	The Regents of the University of California.  All rights reserved.
 */

/*
 * List declarations.
 */
#define	LIST_HEAD(name, type)						\
struct name {								\
	struct type *lh_first;	/* first element */			\
}

#define	LIST_ENTRY(type)						\
struct {								\
	struct type *le_next;	/* next element */			\
	struct type **le_prev;	/* address of previous next element */	\
}

/*
 * List functions.
 */

#define	LIST_FIRST(head)	((head)->lh_first)

#define	LIST_FOREACH(var, head, field)					\
	for ((var) = LIST_FIRST((head));				\
	    (var);							\
	    (var) = LIST_NEXT((var), field))

#define	LIST_FOREACH_SAFE(var, head, field, tvar)			\
	for ((var) = LIST_FIRST((head));				\
	    (var) && ((tvar) = LIST_NEXT((var), field), 1);		\
	    (var) = (tvar))

#define	LIST_INIT(head) do {						\
	LIST_FIRST((head)) = NULL;					\
} while (0)

#define	LIST_INSERT_HEAD(head, elm, field) do {				\
	if ((LIST_NEXT((elm), field) = LIST_FIRST((head))) != NULL)	\
		LIST_FIRST((head))->field.le_prev = &LIST_NEXT((elm), field);\
	LIST_FIRST((head)) = (elm);					\
	(elm)->field.le_prev = &LIST_FIRST((head));			\
} while (0)

#define	LIST_NEXT(elm, field)	((elm)->field.le_next)

#define	LIST_REMOVE(elm, field) do {					\
	if (LIST_NEXT((elm), field) != NULL)				\
		LIST_NEXT((elm), field)->field.le_prev = 		\
		    (elm)->field.le_prev;				\
	*(elm)->field.le_prev = LIST_NEXT((elm), field);		\
} while (0)

/*********************************************************************/

struct clikit_prefix;
struct clikit_branch;

struct clikit {
	unsigned			magic;
#define CLIKIT_MAGIC			0x6c5315b8
	LIST_HEAD(, clikit_branch)	branches;
	LIST_HEAD(, clikit_prefix)	prefixes;
	LIST_HEAD(, clikit_context)	contexts;
};

struct clikit_branch {
	unsigned			magic;
#define CLIKIT_BRANCH_MAGIC		0x21031be5
	LIST_ENTRY(clikit_branch)	list;
	clikit_match_f			*func;
	char				*root;
};

struct clikit_prefix {
	unsigned			magic;
#define CLIKIT_PREFIX_MAGIC		0xb793beea
	LIST_ENTRY(clikit_prefix)	list;
	char				*pfx;
	unsigned			val;
};

struct clikit_context {
	unsigned			magic;
#define CLIKIT_CONTEXT_MAGIC		0xa70f836a
	struct clikit			*ck;
	LIST_ENTRY(clikit_context)	list;
	char				*b;
	char				*e;
	char				*p;
	enum {
		sIdle,
		sComment,
		sWord,
		sQuoted,
		sBackslash
	}				st;
};

/*********************************************************************/

struct clikit *
CLIkit_New(void)
{
	struct clikit *ck;

	ck = calloc(1L, sizeof *ck);
	if (ck == NULL)
		return (ck);
	ck->magic = CLIKIT_MAGIC;
	LIST_INIT(&ck->branches);
	LIST_INIT(&ck->prefixes);
	LIST_INIT(&ck->contexts);
	return (ck);
}

int
CLIkit_Destroy(struct clikit *ck)
{
	struct clikit_branch *cb, *cb2;
	struct clikit_prefix *cp, *cp2;
	struct clikit_context *cc, *cc2;
	int retval = 0;

	assert(ck != NULL && ck->magic == CLIKIT_MAGIC);

	LIST_FOREACH_SAFE(cc, &ck->contexts, list, cc2) {
		assert(cc != NULL && cc->magic == CLIKIT_CONTEXT_MAGIC);
		retval |= CLIkit_Destroy_Context(cc);
	}
		
	LIST_FOREACH_SAFE(cb, &ck->branches, list, cb2) {
		assert(cb != NULL && cb->magic == CLIKIT_BRANCH_MAGIC);
		retval |= CLIkit_Del_Tree(ck, cb->func, cb->root);
	}
		
	LIST_FOREACH_SAFE(cp, &ck->prefixes, list, cp2) {
		assert(cp != NULL && cp->magic == CLIKIT_PREFIX_MAGIC);
		retval |= CLIkit_Del_Prefix(ck, cp->pfx);
	}

	free(ck);
	return (retval);
}

/*********************************************************************/

int
CLIkit_Add_Prefix(struct clikit *ck, const char *pfx, unsigned val)
{
	struct clikit_prefix *cp;
	struct clikit_branch *cb;

	assert(ck != NULL && ck->magic == CLIKIT_MAGIC);

	LIST_FOREACH(cp, &ck->prefixes, list) {
		assert(strcmp(cp->pfx, pfx));
		assert(cp->val != val);
	}
	LIST_FOREACH(cb, &ck->branches, list)
		assert(strcmp(cb->root, pfx));

	cp = calloc(1L, sizeof *cp);
	if (cp == NULL)
		return (-1);
	cp->magic = CLIKIT_PREFIX_MAGIC;
	cp->val = val;
	cp->pfx = strdup(pfx);
	if (cp->pfx == NULL) {
		free(cp);
		return (-1);
	}
	LIST_INSERT_HEAD(&ck->prefixes, cp, list);
	return (0);
}

int
CLIkit_Del_Prefix(const struct clikit *ck, const char *pfx)
{
	struct clikit_prefix *cp;
	
	assert(ck != NULL && ck->magic == CLIKIT_MAGIC);
	LIST_FOREACH(cp, &ck->prefixes, list) {
		assert(cp != NULL && cp->magic == CLIKIT_PREFIX_MAGIC);
		if (!strcmp(cp->pfx, pfx)) {
			LIST_REMOVE(cp, list);
			free(cp->pfx);
			free(cp);
			return (0);
		}
	}
	return (-1);
}

/*********************************************************************/

int
CLIkit_Add_Tree(struct clikit *ck, clikit_match_f *func,
    const char *root)
{
	struct clikit_branch *cb;
	struct clikit_prefix *cp;

	assert(ck != NULL && ck->magic == CLIKIT_MAGIC);

	if (root != NULL) {
		LIST_FOREACH(cp, &ck->prefixes, list)
			assert(strcmp(cp->pfx, root));
		LIST_FOREACH(cb, &ck->branches, list)
			assert(strcmp(cb->root, root));
	}
	cb = calloc(1L, sizeof *cb);
	if (cb == NULL)
		return (-1);
	cb->magic = CLIKIT_BRANCH_MAGIC;
	cb->func = func;
	if (root != NULL) {
		cb->root = strdup(root);
		if (cb->root == NULL) {
			free(cb);
			return (-1);
		}
	}
	LIST_INSERT_HEAD(&ck->branches, cb, list);
	return (0);
}

int
CLIkit_Del_Tree(const struct clikit *ck, clikit_match_f *func,
    const char *root)
{
	struct clikit_branch *cb;
	
	assert(ck != NULL && ck->magic == CLIKIT_MAGIC);
	LIST_FOREACH(cb, &ck->branches, list) {
		assert(cb != NULL && cb->magic == CLIKIT_BRANCH_MAGIC);
		if (cb->func != func)
			continue;
		if (cb->root == NULL && root == NULL)
			;
		else if (cb->root == NULL || root == NULL)
			continue;
		else if (strcmp(cb->root, root)) 
			continue;

		LIST_REMOVE(cb, list);
		free(cb->root);
		free(cb);
		return (0);
	}
	return (-1);
}

/*********************************************************************/

struct clikit_context *
CLIkit_New_Context(struct clikit *ck)
{
	struct clikit_context *cc;

	assert(ck != NULL && ck->magic == CLIKIT_MAGIC);

	cc = calloc(1L, sizeof *cc);
	if (cc == NULL)
		return (NULL);
	cc->magic = CLIKIT_CONTEXT_MAGIC;
	cc->ck = ck;
	cc->b = malloc(64L);
	if (cc->b == NULL) {
		free(cc);
		return (NULL);
	}
	cc->e = cc->b + 64;
	cc->p = cc->b;
	cc->st = sIdle;
	LIST_INSERT_HEAD(&ck->contexts, cc, list);

	return (cc);
}

int
CLIkit_Destroy_Context(struct clikit_context *cc)
{
	struct clikit *ck;
	
	assert(cc != NULL && cc->magic == CLIKIT_CONTEXT_MAGIC);
	ck = cc->ck;
	assert(ck != NULL && ck->magic == CLIKIT_MAGIC);
	LIST_REMOVE(cc, list);
	(void)memset(cc, 0, sizeof *cc);
	free(cc);
	return (0);
}

/*********************************************************************/

#include <ctype.h>		/* XXX */
#include <stdio.h>		/* XXX */
/*lint -esym(534,printf) */

static void
clikit_add_char(struct clikit_context *cc, int ch)
{
	int l;
	char *p;

	assert(cc != NULL && cc->magic == CLIKIT_CONTEXT_MAGIC);
	assert(cc->b < cc->e);
	assert(cc->p >= cc->b);
	assert(cc->p <= cc->e);

	if (cc->p == cc->e) {
		l = cc->e - cc->b;
		if (l > 4096L)
			l += 4096L;
		else
			l += l;
		p = realloc(cc->b, (size_t)l);
		/* XXX: p */
		assert(p != NULL);
		cc->p = p + (cc->p - cc->b);
		cc->b = p;
		cc->e = p + l;
	}
	assert(cc->p >= cc->b);
	assert(cc->p < cc->e);
	*cc->p = (char)ch;
	cc->p++;
}

static void
clikit_complete(struct clikit_context *cc)
{
	char *p;

	assert(cc != NULL && cc->magic == CLIKIT_CONTEXT_MAGIC);
	clikit_add_char(cc, 0);
	printf("\\nZZ: %ld\\n", (cc->p - cc->b));
	
	for (p = cc->b; p < cc->p; p += strlen(p) + 1)
		printf("\\t{%s}\\n", p);

	cc->p = cc->b;
	cc->st = sIdle;
}

static void
clikit_in_char(struct clikit_context *cc, int ch)
{

	assert(cc != NULL && cc->magic == CLIKIT_CONTEXT_MAGIC);
	if (ch >= ' ' && ch <= '~')
		printf("%d, %c\\t", cc->st, ch);
	else
		printf("%d, 0x%02x\\t", cc->st, ch);

	switch(cc->st) {
	case sIdle:
		if (ch == '#')
			cc->st = sComment;
		else if (isspace(ch)) {
			cc->st = sIdle;
		} else if (ch == '"')
			cc->st = sQuoted;
		else {
			cc->st = sWord;
			clikit_add_char(cc, ch);
		}
		break;
	case sWord:
		if (isspace(ch)) {
			clikit_add_char(cc, 0);
			cc->st = sIdle;
			if (!isblank(ch))
				clikit_complete(cc);
		} else {
			clikit_add_char(cc, ch);
		}
		break;
	case sQuoted:
		if (ch == '"') {
			clikit_add_char(cc, 0);
			cc->st = sIdle;
		} else if (ch == '\\\\') {
			cc->st = sBackslash;
		} else {
			clikit_add_char(cc, ch);
		}
		break;
	case sBackslash:
		if (ch == 'n') {
			clikit_add_char(cc, '\\n');
		} else {
			clikit_add_char(cc, ch);
		}
		cc->st = sQuoted;
		break;
	case sComment:
		if (isblank(ch))
			;
		else if (isspace(ch))
			cc->st = sIdle;
		break;
	default:
		break;
	}  
	if (ch >= ' ' && ch <= '~')
		printf("%d, %c\\n", cc->st, ch);
	else
		printf("%d, 0x%02x\\n", cc->st, ch);
}

void
CLIkit_Input(struct clikit_context *cc, const char *s)
{

	assert(cc != NULL && cc->magic == CLIKIT_CONTEXT_MAGIC);
	while (*s != 0)
		clikit_in_char(cc, *s++);
}

/*********************************************************************/

int
clikit_int_match(struct clikit_context *cc, const char *str)
{
	(void)cc;
	(void)str;
	return (-1);
}

int
clikit_int_eol(struct clikit_context *cc)
{
	(void)cc;
	return (-1);
}

void
clikit_int_push_instance(struct clikit_context *cc)
{
	(void)cc;
}

void
clikit_int_pop_instance(struct clikit_context *cc)
{
	(void)cc;
}

int
clikit_int_unknown(struct clikit_context *cc)
{
	(void)cc;
	return (-1);
}

int
clikit_int_arg_REAL(struct clikit_context *cc, double *arg)
{
	(void)cc;
	(void)arg;
	return (-1);
}

int
clikit_int_arg_INT(struct clikit_context *cc, int *arg)
{
	(void)cc;
	(void)arg;
	return (-1);
}

int
clikit_int_arg_UINT(struct clikit_context *cc, unsigned *arg)
{
	(void)cc;
	(void)arg;
	return (-1);
}

int
clikit_int_arg_WORD(struct clikit_context *cc, const char **arg)
{
	(void)cc;
	(void)arg;
	return (-1);
}


""")

#######################################################################
#######################################################################
#

import shlex

def syntax(foo):
	sys.stderr.write("Syntax Error:\n\t" + foo + "\n")
	exit(2)

def keyval(kv, tl, id):
	assert len(tl) > 0
	if not tl[0] in kv:
		return False
	i = tl.pop(0)
	if kv[i] != None:
		syntax("Multiple '%s' in %s" % (i, id))
	if len(tl) == 0:
		syntax("Missing value '%s' %s" % (i, id))
	kv[i] = tl.pop(0)
	return True

def parse_leaf(tl, fc, fh):
	assert tl.pop(0) == "LEAF"
	nr = len(tl)
	nm = tl.pop(0)

	fh.write("/* At token %d LEAF %s */\n" % (nr, nm))
	fc.write("\n/* At token %d LEAF %s */\n" % (nr, nm))

	al = list()
	while len(tl) > 0 and tl[0] != "{":
		if tl[0] not in types:
			syntax("Bad type '%s' in LEAF(%s)" % (tl[0], nm))
		al.append(tl.pop(0))
	if len(tl) == 0:
		syntax("Missing '{' in LEAF(%s)" % nm)
	assert tl.pop(0) == "{"
	kv = {
		"desc":	None,
		"func": None,
		"name": None,
	}
	while len(tl) > 0 and tl[0] != "}":
		if keyval(kv, tl, "LEAF(%s)" % nm):
			continue
		else:
			syntax("Unknown '%s' in LEAF(%s)" % (tl[0], nm))
	if len(tl) == 0:
		syntax("Missing '}' in LEAF(%s)" % nm)
	assert tl.pop(0) == "}"

	if kv['name'] == None:
		kv['name'] = "match_%d" % nr
		static = "static "
	else:
		static = ""
		fh.write("int %s(struct clikit_context*);\n" % kv['name'])

	if kv['func'] == None:
		syntax("Missing 'func' in LEAF(%s)" % nm)

	print("Leaf(%d, %s)" % (nr, nm), al, kv)

	fh.write("void %s(struct clikit_context *" % kv["func"])
	for i in al:
		fh.write(", %s" % types[i]);
	fh.write(");\n\n")

	fc.write(static + "int\n%s(struct clikit_context *cc)\n" % kv['name'])
	fc.write('{\n')
	n = 0
	for i in al:
		fc.write("\t%s arg_%d;\n" % (types[i], n))
		n += 1
	fc.write("\n")	
	fc.write('\tif (clikit_int_match(cc, "%s"))\n\t\treturn(0);\n' % nm)
	n = 0
	for i in al:
		fc.write('\tif (clikit_int_arg_%s(cc, &arg_%d))\n' % (i, n))
		fc.write('\t\treturn(-1);\n')
		n += 1
	fc.write('\tif (!clikit_int_eol(cc))\n\t\treturn(-1);\n')
	fc.write('\t%s(cc' % kv['func'])
	n = 0
	for i in al:
		fc.write(", arg_%d" % n)
		n += 1
	fc.write(");\n")
	fc.write("\treturn(1);\n")
	fc.write("}\n")

	return kv['name']
	

def parse_instance(tl, fc, fh):
	assert tl.pop(0) == "INSTANCE"
	nr = len(tl)
	nm = tl.pop(0)

	al = list()
	children = list()
	while len(tl) > 0 and tl[0] != "{":
		if tl[0] not in types:
			syntax("Bad type '%s' in LEAF(%s)" % (tl[0], nm))
		al.append(tl.pop(0))
	if len(tl) == 0:
		syntax("Missing '{' in INSTANCE(%s)" % nm)
	assert tl.pop(0) == "{"
	kv = {
		"desc":	None,
		"func": None,
		"name": None,
	}
	while len(tl) > 0 and tl[0] != "}":
		if keyval(kv, tl, "INSTANCE(%s)" % nm):
			continue
		elif tl[0] == "LEAF":
			children.append(parse_leaf(tl, fc, fh))
		elif tl[0] == "INSTANCE":
			children.append(parse_instance(tl, fc, fh))
		else:
			syntax("Unknown '%s' in INSTANCE(%s)" % (tl[0], nm))
	if len(tl) == 0:
		syntax("Missing '}' in LEAF(%s)" % nm)
	assert tl.pop(0) == "}"

	fh.write("/* At token %d INSTANCE %s */\n" % (nr, nm))
	fc.write("\n/* At token %d INSTANCE %s */\n" % (nr, nm))

	if kv['name'] == None:
		kv['name'] = "match_%d" % nr
		static = "static "
	else:
		static = ""
		fh.write("int %s(struct clikit_context*);\n" % kv['name'])

	if kv['func'] == None:
		syntax("Missing 'func' in LEAF(%s)" % nm)

	print("Instance(%d, %s)" % (nr, nm), al, kv)
	for i in children:
		print("\t", i)
		
	fh.write("int %s(struct clikit_context *" % kv["func"])
	for i in al:
		fh.write(", %s" % types[i]);
	fh.write(");\n\n")

	fc.write(static + "int\n%s(struct clikit_context *cc)\n" % kv['name'])
	fc.write('{\n')
	fc.write('\tint retval;\n')
	n = 0
	for i in al:
		fc.write("\t%s arg_%d;\n" % (types[i], n))
		n += 1
	fc.write("\n")	
	fc.write('\tif (clikit_int_match(cc, "%s"))\n\t\treturn(0);\n' % nm)
	n = 0
	for i in al:
		fc.write('\tif (clikit_int_arg_%s(cc, &arg_%d))\n' % (i, n))
		fc.write('\t\treturn(-1);\n')
		n += 1
	fc.write("\tclikit_int_push_instance(cc);\n")
	fc.write("\tif (%s(cc" % kv['func'])
	n = 0
	for i in al:
		fc.write(", arg_%d" % n)
		n += 1
	fc.write("))\n")
	fc.write("\t\tretval = -1;\n")
	fc.write('\telse if (clikit_int_eol(cc))\n')
	fc.write("\t\tretval = 1;\n")
	s = ""
	for i in children:
		print(i)
		fc.write("\t" + s)
		fc.write("if ((retval = %s(cc)) != 0) /*lint !e838*/\n" % i)
		fc.write("\t\t;\n")
		s = "else "
	fc.write("\telse\n")
	fc.write("\t\tretval = clikit_int_unknown(cc);\n")
	fc.write("\tclikit_int_pop_instance(cc);\n")
	fc.write("\treturn (retval);\n")
	fc.write("}\n");

	return kv['name']


def parse(fname, fc, fh):
	fi = open(fname, "r")
	pt = fi.read()
	fi.close()
	tl = shlex.split(pt, "#")
	children = list()
	while len(tl):
		i = tl[0]
		if i == "LEAF":
			children.append(parse_leaf(tl, fc, fh))
		elif i == "INSTANCE":
			children.append(parse_instance(tl, fc, fh))
		else:
			syntax("Unknown '%s' at top" % tl[0])

	if len(children) == 0:
		return

	fh.write("/* At top BRANCH */\n")
	fc.write("\n/* At top BRANCH */\n")

	fh.write("int clikit_match(struct clikit_context *);\n")

	fc.write("int\nclikit_match(struct clikit_context *cc)\n")
	fc.write("{\n")
	fc.write("\tint retval;\n")
	fc.write("\n")
	s = ""
	for i in children:
		print(i)
		fc.write("\t" + s)
		fc.write("if ((retval = %s(cc)) != 0) /*lint !e838*/\n" % i)
		fc.write("\t\t;\n")
		s = "else "
	fc.write("\telse\n")
	fc.write("\t\tretval = 0;\n")
	fc.write("\treturn (retval);\n")
	fc.write("}\n")


#######################################################################
#

def do_tree(argv):
	print("DO_TREE", argv)
	if len(argv) != 1:
		usage("XXX: options not yet implemented")
	fname = os.path.splitext(argv[0])

	fc = open(fname[0] + ".c", "w")
	do_copyright(fc)

	fc.write('#define CLIKIT_INTERNAL\n')
	fc.write('#include "clikit.h"\n')
	fc.write('#include "%s.h"\n' % fname[0])

	fh = open(fname[0] + ".h", "w")
	do_copyright(fh)

	parse(argv[0], fc, fh)
	print(fname)
	fc.close()
	fh.close()

#######################################################################
#######################################################################
#

if __name__ == "__main__":
	if len(sys.argv) < 2:
		usage("Need at least one argument")
	elif sys.argv[1] == "--code":
		do_code(sys.argv [2:])
	elif sys.argv[1] == "--tree":
		do_tree(sys.argv [2:])
	else:
		usage("Argument error")
