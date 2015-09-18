# -*- coding: utf-8 -*-

# Copyright (c) 2014, KOL
# All rights reserved.

# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of the <organization> nor the
#       names of its contributors may be used to endorse or promote products
#       derived from this software without specific prior written permission.

# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTLICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL <COPYRIGHT HOLDER> BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

from updater import Updater
Common = SharedCodeService.common


def Start():
    HTTP.CacheTime = CACHE_1HOUR


###############################################################################
# Video
###############################################################################

@handler(
    Common.PREFIX,
    L(Common.TITLE),
    None,
    R(Common.ICON)
)
def MainMenu():

    cache = Data.LoadObject(Common.KEY_CACHE) or {}
    channels = Common.GetChannels(cache)

    if not channels:
        return MessageContainer(
            L('Error'),
            L('Service not avaliable')
        )

    oc = ObjectContainer(title2=L(Common.TITLE), no_cache=True)

    Updater(Common.PREFIX+'/update', oc)

    cache = {}
    for channel in channels:
        cache[channel['id']] = channel
        oc.add(DirectoryObject(
            key=Callback(Channel, uri=channel['URI']),
            title=channel['title'],
            thumb=channel['thumb']
        ))

    Data.SaveObject(Common.KEY_CACHE, cache)

    return oc


@route(Common.PREFIX + '/channel')
def Channel(uri):
    item = Common.GetChannel(uri)

    if not item:
        return ContentNotFound()

    # Update cache
    channel = Common.GetChannelObject(uri, item)
    cache = Data.LoadObject(Common.KEY_CACHE) or {}
    cache[channel['id']] = channel
    Data.SaveObject(Common.KEY_CACHE, cache)

    oc = ObjectContainer(title2=u'%s' % channel['title'])

    for video in item['videos']:
        oc.add(Common.GetVideoObject(video))

    return oc if len(oc) else ContentNotFound()


###############################################################################
# Common
###############################################################################

def ContentNotFound():
    return MessageContainer(
        L('Error'),
        L('No entries found')
    )