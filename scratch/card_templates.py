import sys
import io
import re
from bs4 import BeautifulSoup

# sys.stdout utf-8

CARDS_HTML = {
    "u2_rev_ex2": """
<div id="ex2-rev-card" class="bg-white rounded-2xl border border-slate-200 p-5 reader-card space-y-4">
  <div class="flex items-center justify-between border-b border-slate-100 pb-3">
    <div class="flex items-center gap-2">
      <span class="w-7 h-7 rounded-lg bg-teal-500 text-white font-bold flex items-center justify-center text-xs shadow-sm">2</span>
      <h4 class="font-bold text-slate-800 text-sm">Complete with Simple Past, Past Progressive, or Used To (Page 53)</h4>
    </div>
    <span class="ex-score text-xs font-bold text-teal-600 bg-teal-50 px-2.5 py-1 rounded-full border border-teal-100">Score: -/7</span>
  </div>
  <p class="text-xs text-slate-600">Complete each sentence or question with the word(s) in parentheses. Use the simple past, the past progressive, or <em>used to</em>.</p>
  <div class="space-y-3 text-xs sm:text-sm">
    <div class="p-2.5 bg-slate-50 rounded-xl border border-slate-100 text-slate-700">
      <span class="font-bold text-slate-400 mr-1.5">1.</span> While I was sitting in the airport lounge, I <strong class="text-emerald-700">saw</strong> (see) a famous actor. <span class="text-slate-400 italic text-[11px]">(Example)</span>
    </div>
    <div class="p-2.5 bg-slate-50 rounded-xl border border-slate-100 text-slate-700">
      <span class="font-bold text-slate-400 mr-1.5">2.</span> Irina <input type="text" class="cloze-input input-clean border border-slate-200 rounded-lg px-2 py-1 text-xs w-28 font-semibold text-slate-800 focus:outline-none focus:border-teal-500" data-ans="used to write,wrote" placeholder="write" /> (write) poems, but now she writes short stories instead.
    </div>
    <div class="p-2.5 bg-slate-50 rounded-xl border border-slate-100 text-slate-700">
      <span class="font-bold text-slate-400 mr-1.5">3.</span> Martin <input type="text" class="cloze-input input-clean border border-slate-200 rounded-lg px-2 py-1 text-xs w-28 font-semibold text-slate-800 focus:outline-none focus:border-teal-500" data-ans="was trying,tried" placeholder="try" /> (try) to turn on his computer, but nothing <input type="text" class="cloze-input input-clean border border-slate-200 rounded-lg px-2 py-1 text-xs w-24 font-semibold text-slate-800 focus:outline-none focus:border-teal-500" data-ans="happened" placeholder="happen" /> (happen).
    </div>
    <div class="p-2.5 bg-slate-50 rounded-xl border border-slate-100 text-slate-700">
      <span class="font-bold text-slate-400 mr-1.5">4.</span> When my brother and I <input type="text" class="cloze-input input-clean border border-slate-200 rounded-lg px-2 py-1 text-xs w-20 font-semibold text-slate-800 focus:outline-none focus:border-teal-500" data-ans="were" placeholder="be" /> (be) young, we <input type="text" class="cloze-input input-clean border border-slate-200 rounded-lg px-2 py-1 text-xs w-28 font-semibold text-slate-800 focus:outline-none focus:border-teal-500" data-ans="played,used to play" placeholder="play" /> (play) games with my parents in the evenings.
    </div>
    <div class="p-2.5 bg-slate-50 rounded-xl border border-slate-100 text-slate-700">
      <span class="font-bold text-slate-400 mr-1.5">5.</span> <input type="text" class="cloze-input input-clean border border-slate-200 rounded-lg px-2 py-1 text-xs w-32 font-semibold text-slate-800 focus:outline-none focus:border-teal-500" data-ans="Did you have,Did you use to have" placeholder="you / have" /> (you / have) trouble with the alphabet when you <input type="text" class="cloze-input input-clean border border-slate-200 rounded-lg px-2 py-1 text-xs w-28 font-semibold text-slate-800 focus:outline-none focus:border-teal-500" data-ans="learned,were learning" placeholder="learn" /> (learn) Arabic?
    </div>
    <div class="p-2.5 bg-slate-50 rounded-xl border border-slate-100 text-slate-700">
      <span class="font-bold text-slate-400 mr-1.5">6.</span> We <input type="text" class="cloze-input input-clean border border-slate-200 rounded-lg px-2 py-1 text-xs w-20 font-semibold text-slate-800 focus:outline-none focus:border-teal-500" data-ans="went" placeholder="go" /> (go) to the movies three times last week.
    </div>
    <div class="p-2.5 bg-slate-50 rounded-xl border border-slate-100 text-slate-700">
      <span class="font-bold text-slate-400 mr-1.5">7.</span> I <input type="text" class="cloze-input input-clean border border-slate-200 rounded-lg px-2 py-1 text-xs w-28 font-semibold text-slate-800 focus:outline-none focus:border-teal-500" data-ans="was working" placeholder="work" /> (work) when you <input type="text" class="cloze-input input-clean border border-slate-200 rounded-lg px-2 py-1 text-xs w-20 font-semibold text-slate-800 focus:outline-none focus:border-teal-500" data-ans="called" placeholder="call" /> (call), so I <input type="text" class="cloze-input input-clean border border-slate-200 rounded-lg px-2 py-1 text-xs w-28 font-semibold text-slate-800 focus:outline-none focus:border-teal-500" data-ans="didn't answer,did not answer" placeholder="not answer" /> (not answer) the phone.
    </div>
    <div class="p-2.5 bg-slate-50 rounded-xl border border-slate-100 text-slate-700">
      <span class="font-bold text-slate-400 mr-1.5">8.</span> When Stephanie was a child, she <input type="text" class="cloze-input input-clean border border-slate-200 rounded-lg px-2 py-1 text-xs w-28 font-semibold text-slate-800 focus:outline-none focus:border-teal-500" data-ans="visited,used to visit" placeholder="visit" /> (visit) her grandparents twice a month.
    </div>
  </div>
  <div class="pt-3 border-t border-slate-100 flex items-center justify-between">
    <button type="button" onclick="checkClozeCard('ex2-rev-card')" class="px-4 py-1.5 rounded-lg bg-teal-600 hover:bg-teal-700 text-white font-bold text-xs transition shadow-sm">Check Answers</button>
  </div>
</div>
""",
    "u2_rev_ex5": """
<div id="ex5-rev-card" class="bg-white rounded-2xl border border-slate-200 p-5 reader-card space-y-4">
  <div class="flex items-center justify-between border-b border-slate-100 pb-3">
    <div class="flex items-center gap-2">
      <span class="w-7 h-7 rounded-lg bg-amber-500 text-white font-bold flex items-center justify-center text-xs shadow-sm">5</span>
      <h4 class="font-bold text-slate-800 text-sm">SPEAK. Dangerous Situations (Page 55)</h4>
    </div>
    <span class="text-xs font-semibold text-amber-600 bg-amber-50 px-2.5 py-1 rounded-full border border-amber-100">Discussion</span>
  </div>
  <p class="text-xs text-slate-600">Work with a partner. Think of a dangerous situation that you or someone you know was in. Discuss the questions below:</p>
  <div class="space-y-3">
    <div class="p-3 bg-amber-50/60 rounded-xl border border-amber-100 text-xs text-slate-700 space-y-2">
      <p class="font-medium text-amber-900">• What happened? What were you or the person doing when the situation occurred?</p>
      <p class="font-medium text-amber-900">• What did you or this person do to survive or resolve the situation?</p>
      <p class="font-medium text-amber-900">• Have you ever been close to a wild animal? What should people do if they see a dangerous animal?</p>
    </div>
    <div class="p-3 bg-slate-50 rounded-xl border border-slate-100 space-y-1.5">
      <label class="block text-xs font-bold text-slate-600">Your Story Notes / Reflections:</label>
      <textarea class="w-full h-20 p-2.5 text-xs bg-white border border-slate-200 rounded-lg text-slate-800 focus:outline-none focus:border-teal-500 resize-none" placeholder="e.g. While my cousin was hiking in the mountains, a thunderstorm started..."></textarea>
    </div>
  </div>
</div>
""",
    "u2_l3_ex7": """
<div id="ex7-l3-card" class="bg-white rounded-2xl border border-slate-200 p-5 reader-card space-y-4">
  <div class="flex items-center justify-between border-b border-slate-100 pb-3">
    <div class="flex items-center gap-2">
      <span class="w-7 h-7 rounded-lg bg-amber-500 text-white font-bold flex items-center justify-center text-xs shadow-sm">7</span>
      <h4 class="font-bold text-slate-800 text-sm">SPEAK. Sequential Events with When (Page 43)</h4>
    </div>
    <span class="text-xs font-semibold text-amber-600 bg-amber-50 px-2.5 py-1 rounded-full border border-amber-100">Partner Speaking</span>
  </div>
  <p class="text-xs text-slate-600">Work with a partner. Complete each sentence with your own true experiences using the simple past in both clauses:</p>
  <div class="space-y-2.5 text-xs">
    <div class="p-2.5 bg-slate-50 rounded-xl border border-slate-100 text-slate-700 flex flex-col sm:flex-row sm:items-center gap-2">
      <span class="font-semibold text-slate-800 min-w-[210px]">1. When I woke up this morning,</span>
      <input type="text" class="flex-1 bg-white border border-slate-200 rounded-lg px-2.5 py-1 text-slate-700 placeholder-slate-400" placeholder="e.g., I checked my messages / I called my parents." />
    </div>
    <div class="p-2.5 bg-slate-50 rounded-xl border border-slate-100 text-slate-700 flex flex-col sm:flex-row sm:items-center gap-2">
      <span class="font-semibold text-slate-800 min-w-[210px]">2. When I got to class,</span>
      <input type="text" class="flex-1 bg-white border border-slate-200 rounded-lg px-2.5 py-1 text-slate-700 placeholder-slate-400" placeholder="e.g., I saw my friends / the teacher opened the book." />
    </div>
    <div class="p-2.5 bg-slate-50 rounded-xl border border-slate-100 text-slate-700 flex flex-col sm:flex-row sm:items-center gap-2">
      <span class="font-semibold text-slate-800 min-w-[210px]">3. When I finished my homework,</span>
      <input type="text" class="flex-1 bg-white border border-slate-200 rounded-lg px-2.5 py-1 text-slate-700 placeholder-slate-400" placeholder="e.g., I went for a walk / I watched TV." />
    </div>
  </div>
</div>
""",
    "u2_l2_ex7": """
<div id="ex7-l2-card" class="bg-white rounded-2xl border border-slate-200 p-5 reader-card space-y-4">
  <div class="flex items-center justify-between border-b border-slate-100 pb-3">
    <div class="flex items-center gap-2">
      <span class="w-7 h-7 rounded-lg bg-amber-500 text-white font-bold flex items-center justify-center text-xs shadow-sm">7</span>
      <h4 class="font-bold text-slate-800 text-sm">SPEAK. Past Progressive Questions & Answers (Page 37)</h4>
    </div>
    <span class="text-xs font-semibold text-amber-600 bg-amber-50 px-2.5 py-1 rounded-full border border-amber-100">Partner Speaking</span>
  </div>
  <p class="text-xs text-slate-600">Work with a partner. Take turns asking and answering questions 4, 7, and 8 from exercise 6. Use your own answers, not the answers in the book:</p>
  <div class="space-y-3 text-xs">
    <div class="p-3 bg-slate-50 rounded-xl border border-slate-100 space-y-1.5">
      <div class="font-semibold text-slate-800 flex items-center gap-2">
        <span class="w-5 h-5 rounded-full bg-teal-100 text-teal-700 flex items-center justify-center font-bold text-[10px]">Q4</span>
        <span>Where were you going after class yesterday?</span>
      </div>
      <input type="text" class="w-full bg-white border border-slate-200 rounded-lg px-2.5 py-1 text-slate-700 placeholder-slate-400" placeholder="e.g., I was going to the gym / I was walking home." />
    </div>
    <div class="p-3 bg-slate-50 rounded-xl border border-slate-100 space-y-1.5">
      <div class="font-semibold text-slate-800 flex items-center gap-2">
        <span class="w-5 h-5 rounded-full bg-teal-100 text-teal-700 flex items-center justify-center font-bold text-[10px]">Q7</span>
        <span>What were you doing at 8:00 yesterday evening?</span>
      </div>
      <input type="text" class="w-full bg-white border border-slate-200 rounded-lg px-2.5 py-1 text-slate-700 placeholder-slate-400" placeholder="e.g., I was eating dinner with my family." />
    </div>
    <div class="p-3 bg-slate-50 rounded-xl border border-slate-100 space-y-1.5">
      <div class="font-semibold text-slate-800 flex items-center gap-2">
        <span class="w-5 h-5 rounded-full bg-teal-100 text-teal-700 flex items-center justify-center font-bold text-[10px]">Q8</span>
        <span>Was it raining when you woke up this morning?</span>
      </div>
      <input type="text" class="w-full bg-white border border-slate-200 rounded-lg px-2.5 py-1 text-slate-700 placeholder-slate-400" placeholder="e.g., No, it wasn't. The sun was shining." />
    </div>
  </div>
</div>
""",
    "u2_l1_ex6": """
<div id="ex6-l1-card" class="bg-white rounded-2xl border border-slate-200 p-5 reader-card space-y-4">
  <div class="flex items-center justify-between border-b border-slate-100 pb-3">
    <div class="flex items-center gap-2">
      <span class="w-7 h-7 rounded-lg bg-amber-500 text-white font-bold flex items-center justify-center text-xs shadow-sm">6</span>
      <h4 class="font-bold text-slate-800 text-sm">SPEAK. Simple Past Questions & Answers (Page 29)</h4>
    </div>
    <span class="text-xs font-semibold text-amber-600 bg-amber-50 px-2.5 py-1 rounded-full border border-amber-100">Partner Speaking</span>
  </div>
  <p class="text-xs text-slate-600">Work with a partner. Take turns asking and answering the questions from exercise 5 using your own real answers:</p>
  <div class="p-3 bg-amber-50/60 rounded-xl border border-amber-100 text-xs space-y-1 text-slate-700">
    <p><strong class="text-amber-900">A:</strong> Did your parents give you any money last month?</p>
    <p><strong class="text-amber-900">B:</strong> Yes, they did. / No, they didn't.</p>
    <p><strong class="text-amber-900">A:</strong> Did you do anything fun last night?</p>
    <p><strong class="text-amber-900">B:</strong> Yes, I watched a movie with my friends.</p>
  </div>
  <div class="space-y-1.5">
    <label class="block text-xs font-bold text-slate-600">Partner's Answers / Notes:</label>
    <input type="text" class="w-full bg-slate-50 border border-slate-200 rounded-lg px-2.5 py-1.5 text-xs text-slate-800 placeholder-slate-400" placeholder="Record what your partner said..." />
  </div>
</div>
""",
    "u1_l1_ex5": """
<div id="ex5-l1-card" class="bg-white rounded-2xl border border-slate-200 p-5 reader-card space-y-4">
  <div class="flex items-center justify-between border-b border-slate-100 pb-3">
    <div class="flex items-center gap-2">
      <span class="w-7 h-7 rounded-lg bg-amber-500 text-white font-bold flex items-center justify-center text-xs shadow-sm">5</span>
      <h4 class="font-bold text-slate-800 text-sm">SPEAK. Affirmative & Negative Statements (Page 6)</h4>
    </div>
    <span class="text-xs font-semibold text-amber-600 bg-amber-50 px-2.5 py-1 rounded-full border border-amber-100">Partner Drill</span>
  </div>
  <p class="text-xs text-slate-600">Work with a partner. Take turns making affirmative or negative statements about wedding traditions using the subjects and verbs below:</p>
  <div class="grid grid-cols-2 gap-3 text-xs">
    <div class="p-2.5 bg-slate-50 rounded-xl border border-slate-100">
      <span class="font-bold text-teal-800 block mb-1">Subjects</span>
      <ul class="text-slate-600 space-y-0.5 list-disc list-inside text-[11px]">
        <li>the bride</li>
        <li>the wedding guests</li>
        <li>the groom</li>
        <li>the bride's father</li>
        <li>they / she / he</li>
      </ul>
    </div>
    <div class="p-2.5 bg-slate-50 rounded-xl border border-slate-100">
      <span class="font-bold text-teal-800 block mb-1">Verbs</span>
      <ul class="text-slate-600 space-y-0.5 list-disc list-inside text-[11px]">
        <li>dance</li>
        <li>eat</li>
        <li>go</li>
        <li>live</li>
        <li>pay</li>
        <li>sing / wear</li>
      </ul>
    </div>
  </div>
  <div class="p-3 bg-amber-50/60 rounded-xl border border-amber-100 text-xs text-slate-700">
    <p class="font-medium text-amber-900 mb-1">Examples:</p>
    <p>• <em>The groom pays for the wedding.</em></p>
    <p>• <em>The bride doesn't go to the wedding ceremony.</em></p>
  </div>
  <input type="text" class="w-full bg-slate-50 border border-slate-200 rounded-lg px-2.5 py-1.5 text-xs text-slate-800 placeholder-slate-400" placeholder="Type one of your affirmative or negative sentences here..." />
</div>
""",
    "u1_l1_ex7": """
<div id="ex7-l1-card" class="bg-white rounded-2xl border border-slate-200 p-5 reader-card space-y-4">
  <div class="flex items-center justify-between border-b border-slate-100 pb-3">
    <div class="flex items-center gap-2">
      <span class="w-7 h-7 rounded-lg bg-amber-500 text-white font-bold flex items-center justify-center text-xs shadow-sm">7</span>
      <h4 class="font-bold text-slate-800 text-sm">SPEAK. Wedding Traditions Q&A (Page 7)</h4>
    </div>
    <span class="text-xs font-semibold text-amber-600 bg-amber-50 px-2.5 py-1 rounded-full border border-amber-100">Partner Speaking</span>
  </div>
  <p class="text-xs text-slate-600">Work with a partner. Take turns asking and answering the questions from exercise 6. In your answers, talk about wedding traditions in your own culture or country:</p>
  <div class="p-3 bg-amber-50/60 rounded-xl border border-amber-100 text-xs space-y-1 text-slate-700">
    <p><strong class="text-amber-900">A:</strong> Do all brides wear white dresses?</p>
    <p><strong class="text-amber-900">B:</strong> No, they don't. Some brides wear red dresses.</p>
  </div>
  <input type="text" class="w-full bg-slate-50 border border-slate-200 rounded-lg px-2.5 py-1.5 text-xs text-slate-800 placeholder-slate-400" placeholder="Describe a wedding tradition in your country..." />
</div>
""",
    "u1_l1_ex10": """
<div id="ex10-l1-card" class="bg-white rounded-2xl border border-slate-200 p-5 reader-card space-y-4">
  <div class="flex items-center justify-between border-b border-slate-100 pb-3">
    <div class="flex items-center gap-2">
      <span class="w-7 h-7 rounded-lg bg-amber-500 text-white font-bold flex items-center justify-center text-xs shadow-sm">10</span>
      <h4 class="font-bold text-slate-800 text-sm">SPEAK. Birthday Celebrations (Page 10)</h4>
    </div>
    <span class="text-xs font-semibold text-amber-600 bg-amber-50 px-2.5 py-1 rounded-full border border-amber-100">Partner Speaking</span>
  </div>
  <p class="text-xs text-slate-600">How do people usually celebrate their birthdays in your culture? In your family? Share your answers with a partner using frequency adverbs (<em>always, usually, sometimes, never</em>):</p>
  <div class="p-3 bg-amber-50/60 rounded-xl border border-amber-100 text-xs space-y-1 text-slate-700">
    <p><strong class="text-amber-900">A:</strong> In my country, we usually cook a big meal for our friends.</p>
    <p><strong class="text-amber-900">B:</strong> Really? That's a lot of work! In my family, we always buy a birthday cake.</p>
  </div>
  <input type="text" class="w-full bg-slate-50 border border-slate-200 rounded-lg px-2.5 py-1.5 text-xs text-slate-800 placeholder-slate-400" placeholder="How do you celebrate your birthday? Type your answer..." />
</div>
""",
    "u1_l2_ex7": """
<div id="ex7-l2-card" class="bg-white rounded-2xl border border-slate-200 p-5 reader-card space-y-4">
  <div class="flex items-center justify-between border-b border-slate-100 pb-3">
    <div class="flex items-center gap-2">
      <span class="w-7 h-7 rounded-lg bg-amber-500 text-white font-bold flex items-center justify-center text-xs shadow-sm">7</span>
      <h4 class="font-bold text-slate-800 text-sm">SPEAK. Present Progressive Q&A (Page 15)</h4>
    </div>
    <span class="text-xs font-semibold text-amber-600 bg-amber-50 px-2.5 py-1 rounded-full border border-amber-100">Partner Speaking</span>
  </div>
  <p class="text-xs text-slate-600">Work with a partner. Ask and answer the questions in numbers 1 and 2 from exercise 6 using your own real answers:</p>
  <div class="space-y-2 text-xs">
    <div class="p-2.5 bg-slate-50 rounded-xl border border-slate-100">
      <p class="font-bold text-slate-800 mb-1">1. Is your cell phone ringing right now?</p>
      <input type="text" class="w-full bg-white border border-slate-200 rounded-lg px-2.5 py-1 text-slate-700 placeholder-slate-400" placeholder="e.g., No, it isn't. It's in my bag." />
    </div>
    <div class="p-2.5 bg-slate-50 rounded-xl border border-slate-100">
      <p class="font-bold text-slate-800 mb-1">2. What are you wearing today?</p>
      <input type="text" class="w-full bg-white border border-slate-200 rounded-lg px-2.5 py-1 text-slate-700 placeholder-slate-400" placeholder="e.g., I'm wearing jeans and a white T-shirt." />
    </div>
  </div>
</div>
""",
    "u1_rev_ex4": """
<div id="ex4-rev-card" class="bg-white rounded-2xl border border-slate-200 p-5 reader-card space-y-4">
  <div class="flex items-center justify-between border-b border-slate-100 pb-3">
    <div class="flex items-center gap-2">
      <span class="w-7 h-7 rounded-lg bg-amber-500 text-white font-bold flex items-center justify-center text-xs shadow-sm">4</span>
      <h4 class="font-bold text-slate-800 text-sm">SPEAK. Festivals & Celebrations (Page 21)</h4>
    </div>
    <span class="text-xs font-semibold text-amber-600 bg-amber-50 px-2.5 py-1 rounded-full border border-amber-100">Group Discussion</span>
  </div>
  <p class="text-xs text-slate-600">Work in a small group. Discuss your answers to these questions:</p>
  <div class="space-y-3 text-xs">
    <div class="p-3 bg-amber-50/60 rounded-xl border border-amber-100 text-slate-700 space-y-1.5">
      <p class="font-medium text-amber-900">1. Does La Tomatina sound like something you would like to go to? Why, or why not?</p>
      <p class="font-medium text-amber-900">2. Tell the other members of your group about a special festival or celebration in your town or city.</p>
    </div>
    <div class="space-y-1">
      <label class="block text-xs font-bold text-slate-600">Your Discussion Notes:</label>
      <textarea class="w-full h-20 p-2.5 text-xs bg-slate-50 border border-slate-200 rounded-lg text-slate-800 focus:outline-none focus:border-teal-500 resize-none" placeholder="Notes on your group's discussion..."></textarea>
    </div>
  </div>
</div>
"""
}

print("Card templates defined successfully:", len(CARDS_HTML))
