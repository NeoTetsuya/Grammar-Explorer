import sys
import io
import re
from bs4 import BeautifulSoup

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

CHART_2_1_HTML = """<div class="lg:col-span-5 bg-white rounded-2xl border border-slate-200 p-5 reader-card space-y-3">
  <div class="flex items-center justify-between border-b border-slate-100 pb-2">
    <h4 class="font-bold text-slate-900 text-sm sm:text-base">2.1 Simple Past: Statements</h4>
    <span class="text-xs bg-slate-100 text-slate-600 px-2 py-0.5 rounded font-mono">Page 28</span>
  </div>

  <div class="space-y-3 text-xs">
    <!-- Affirmative Table -->
    <div class="border border-slate-200 rounded-xl overflow-hidden shadow-sm">
      <div class="bg-slate-100 px-3 py-1.5 font-bold text-slate-700 flex items-center justify-between">
        <span>Affirmative Statements</span>
        <span class="text-[10px] text-slate-500 font-normal">Subject + Verb (Past Form)</span>
      </div>
      <table class="w-full text-left">
        <tbody class="divide-y divide-slate-100 text-slate-700">
          <tr>
            <td class="p-2.5 font-medium text-slate-600 bg-slate-50/50 w-1/2">I / He / She</td>
            <td class="p-2.5 font-semibold text-slate-900"><span class="text-teal-700">helped</span> the animals.</td>
          </tr>
          <tr>
            <td class="p-2.5 font-medium text-slate-600 bg-slate-50/50">You / We / They</td>
            <td class="p-2.5 font-semibold text-slate-900"><span class="text-teal-700">went</span> to Africa.</td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Negative Table -->
    <div class="border border-slate-200 rounded-xl overflow-hidden shadow-sm">
      <div class="bg-slate-100 px-3 py-1.5 font-bold text-slate-700 flex items-center justify-between">
        <span>Negative Statements</span>
        <span class="text-[10px] text-slate-500 font-normal">Subject + Did Not / Didn't + Base Form</span>
      </div>
      <table class="w-full text-left">
        <tbody class="divide-y divide-slate-100 text-slate-700">
          <tr>
            <td class="p-2.5 font-medium text-slate-600 bg-slate-50/50 w-1/2">I / He / She</td>
            <td class="p-2.5 font-semibold text-slate-900"><span class="text-rose-600">didn’t / did not</span> help them.</td>
          </tr>
          <tr>
            <td class="p-2.5 font-medium text-slate-600 bg-slate-50/50">You / We / They</td>
            <td class="p-2.5 font-semibold text-slate-900"><span class="text-rose-600">didn’t / did not</span> go to China.</td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Uses -->
    <div class="bg-slate-50 p-3 rounded-xl border border-slate-200 space-y-1.5 leading-relaxed text-slate-700">
      <span class="font-bold text-slate-800 block text-[11px] uppercase tracking-wide">Use the Simple Past for:</span>
      <p>• <strong>Completed action or event:</strong> <em>She called me yesterday.</em></p>
      <p>• <strong>Regular or repeated action in the past:</strong> <em>I worked every day last week.</em></p>
      <p>• <strong>Past states or feelings:</strong> <em>He felt sick this morning.</em></p>
    </div>

    <!-- Regular & Irregular Form Guide -->
    <div class="p-2.5 bg-slate-50 rounded-xl border border-slate-200 space-y-1 text-slate-700">
      <p><strong>Regular verbs:</strong> Add <em>-ed</em> or <em>-d</em> to base form (<em class="text-slate-900">play ➔ played, dance ➔ danced</em>).</p>
      <p><strong>Irregular verbs:</strong> Many common verbs have irregular past forms (<em class="text-slate-900">eat ➔ ate, make ➔ made, go ➔ went, see ➔ saw</em>).</p>
      <p class="text-[11px] text-slate-500 pt-1 border-t border-slate-200 italic">See page A2 for spelling rules and page A4 for a complete list of irregular verbs.</p>
    </div>

    <!-- Forms of Be (Was / Were) -->
    <div class="bg-amber-50/80 p-3 rounded-xl border border-amber-200 text-amber-950 space-y-1.5">
      <div class="flex items-center gap-1.5 font-bold text-amber-900">
        <svg class="w-4 h-4 text-amber-600 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/></svg>
        <span>Be Careful! Forms of 'be' (was / were)</span>
      </div>
      <p>The simple past forms of <em>be</em> are <strong>was</strong> and <strong>were</strong> (<em>It was warm / It wasn’t cold; They were at work / They weren’t at home</em>).</p>
      <p class="font-semibold text-rose-700">Do NOT use <em>did not</em> or <em>didn’t</em> with was/were in the negative!</p>
      <p class="font-mono text-[11px] text-emerald-800">✓ I wasn’t late for class yesterday.</p>
      <p class="font-mono text-[11px] text-rose-600">✗ I didn’t was late for class yesterday.</p>
    </div>
  </div>
</div>"""

CHART_2_2_HTML = """<div class="lg:col-span-5 bg-white rounded-2xl border border-slate-200 p-5 reader-card space-y-3">
  <div class="flex items-center justify-between border-b border-slate-100 pb-2">
    <h4 class="font-bold text-slate-900 text-sm sm:text-base">2.2 Simple Past: Questions and Answers</h4>
    <span class="text-xs bg-slate-100 text-slate-600 px-2 py-0.5 rounded font-mono">Page 29</span>
  </div>

  <div class="space-y-3 text-xs">
    <!-- Yes/No Questions Table -->
    <div class="border border-slate-200 rounded-xl overflow-hidden shadow-sm">
      <div class="bg-slate-100 px-3 py-1.5 font-bold text-slate-700 flex items-center justify-between">
        <span>Yes / No Questions</span>
        <span class="text-[10px] text-slate-500 font-normal">Short Answers</span>
      </div>
      <div class="p-2.5 bg-white space-y-2 text-slate-700">
        <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-1 border-b border-slate-100 pb-1.5">
          <span><strong>Did</strong> she / I / he / it <strong>help</strong>?</span>
          <span class="text-slate-600 font-medium">→ <em>Yes, she did. / No, she didn’t.</em></span>
        </div>
        <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-1">
          <span><strong>Did</strong> they / we / you <strong>help</strong>?</span>
          <span class="text-slate-600 font-medium">→ <em>Yes, they did. / No, they didn’t.</em></span>
        </div>
      </div>
    </div>

    <!-- Wh- Questions Table -->
    <div class="border border-slate-200 rounded-xl overflow-hidden shadow-sm">
      <div class="bg-slate-100 px-3 py-1.5 font-bold text-slate-700 flex items-center justify-between">
        <span>Wh- Questions (Information)</span>
        <span class="text-[10px] text-slate-500 font-normal">Wh- + Did + Subject + Base Form</span>
      </div>
      <div class="p-2.5 bg-white space-y-1.5 text-slate-700">
        <p>• <strong>When did</strong> you call? → <em class="text-slate-900 font-medium">This morning.</em></p>
        <p>• <strong>Why did</strong> she leave? → <em class="text-slate-900 font-medium">Because she had a meeting.</em></p>
        <p>• <strong>Who(m) did</strong> they see? → <em class="text-slate-900 font-medium">Nick and Sarah.</em></p>
        <p class="text-[11px] text-slate-500 italic pt-1 border-t border-slate-100">* <em>Whom</em> is sometimes used as object in very formal speech/writing (<em>Whom did you ask?</em>).</p>
      </div>
    </div>

    <!-- Who / What as Subject -->
    <div class="border border-amber-200 rounded-xl overflow-hidden bg-amber-50/60 shadow-sm">
      <div class="bg-amber-100/80 px-3 py-1.5 font-bold text-amber-900 flex items-center justify-between">
        <span>Who or What as Subject</span>
        <span class="text-[10px] text-amber-800 font-normal">Who/What + Past Form</span>
      </div>
      <div class="p-2.5 space-y-1.5 text-slate-800">
        <div class="flex items-center justify-between">
          <span>• <strong>Who called</strong>?</span>
          <span class="text-slate-600 font-medium">→ <em>My sister.</em></span>
        </div>
        <div class="flex items-center justify-between">
          <span>• <strong>What happened</strong>?</span>
          <span class="text-slate-600 font-medium">→ <em>I missed the train.</em></span>
        </div>
        <div class="mt-2 pt-2 border-t border-amber-200 text-rose-600 text-[11px] font-semibold">
          ⚠️ <strong>Be careful!</strong> When Who or What is the subject, do NOT use <em>did</em>!
        </div>
        <div class="text-[11px] space-y-0.5">
          <p class="text-emerald-800 font-mono">✓ Who called?</p>
          <p class="text-rose-600 font-mono">✗ Who did call?</p>
        </div>
      </div>
    </div>

    <!-- Real English Time Expressions -->
    <div class="bg-slate-50 p-2.5 rounded-xl border border-slate-200 text-slate-700 space-y-1">
      <strong class="text-slate-800 block text-[11px] uppercase tracking-wide">Real English: Past Time Expressions</strong>
      <p>Expressions such as <em>last night, last week, two days ago, six months ago, in 2011</em> are often used with simple past (e.g. <em>I saw Kim two days ago. She swam every day last year.</em>).</p>
    </div>
  </div>
</div>"""

CHART_2_3_HTML = """<div class="lg:col-span-5 bg-white rounded-2xl border border-slate-200 p-5 reader-card space-y-3">
  <div class="flex items-center justify-between border-b border-slate-100 pb-2">
    <h4 class="font-bold text-slate-900 text-sm sm:text-base">2.3 Past Progressive: Statements</h4>
    <span class="text-xs bg-slate-100 text-slate-600 px-2 py-0.5 rounded font-mono">Page 35</span>
  </div>

  <div class="space-y-3 text-xs">
    <!-- Affirmative Table -->
    <div class="border border-slate-200 rounded-xl overflow-hidden shadow-sm">
      <div class="bg-slate-100 px-3 py-1.5 font-bold text-slate-700 flex items-center justify-between">
        <span>Affirmative Statements</span>
        <span class="text-[10px] text-slate-500 font-normal">Subject + Was/Were + Verb-ing</span>
      </div>
      <table class="w-full text-left">
        <tbody class="divide-y divide-slate-100 text-slate-700">
          <tr>
            <td class="p-2 font-medium text-slate-600 bg-slate-50/50 w-2/5">I / He / She / It</td>
            <td class="p-2 font-semibold text-slate-900"><span class="text-teal-700">was working</span>.</td>
          </tr>
          <tr>
            <td class="p-2 font-medium text-slate-600 bg-slate-50/50">You / We / They</td>
            <td class="p-2 font-semibold text-slate-900"><span class="text-teal-700">were working</span>.</td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Negative Table -->
    <div class="border border-slate-200 rounded-xl overflow-hidden shadow-sm">
      <div class="bg-slate-100 px-3 py-1.5 font-bold text-slate-700 flex items-center justify-between">
        <span>Negative Statements</span>
        <span class="text-[10px] text-slate-500 font-normal">Subject + Was/Were Not + Verb-ing</span>
      </div>
      <table class="w-full text-left">
        <tbody class="divide-y divide-slate-100 text-slate-700">
          <tr>
            <td class="p-2 font-medium text-slate-600 bg-slate-50/50 w-2/5">I / He / She / It</td>
            <td class="p-2 font-semibold text-slate-900"><span class="text-rose-600">was not / wasn't</span> sleeping.</td>
          </tr>
          <tr>
            <td class="p-2 font-medium text-slate-600 bg-slate-50/50">You / We / They</td>
            <td class="p-2 font-semibold text-slate-900"><span class="text-rose-600">were not / weren't</span> sleeping.</td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Uses & Contrast -->
    <div class="bg-slate-50 p-3 rounded-xl border border-slate-200 space-y-1.5 text-slate-700 leading-relaxed">
      <span class="font-bold text-slate-800 block text-[11px] uppercase tracking-wide">Past Progressive Usage:</span>
      <p>• <strong>Action in progress at a certain time in the past:</strong> <em>They were studying at 9:00 last night.</em></p>
      <div class="pt-2 border-t border-slate-200 space-y-1">
        <span class="font-bold text-slate-800 block text-[11px] uppercase tracking-wide">Contrast with Simple Past:</span>
        <p>• <em>Yesterday I rode my bike to work.</em> (completed action)</p>
        <p>• <em>She swam every day last week.</em> (repeated past action)</p>
        <p>• <em>He didn’t like the movie.</em> (past state/feeling)</p>
      </div>
    </div>

    <!-- Non-Action Verbs Callout -->
    <div class="border border-rose-200 rounded-xl p-2.5 bg-rose-50/70 text-rose-950 space-y-1">
      <strong class="text-rose-900 block font-semibold">Non-Action Verbs:</strong>
      <p>Stative verbs (see, like, understand, own) are <strong>not</strong> usually used with the progressive.</p>
      <p class="font-mono text-[11px] text-emerald-800">✓ I saw an accident last night.</p>
      <p class="font-mono text-[11px] text-rose-600">✗ I was seeing an accident last night.</p>
    </div>

    <!-- Real English Scene Description -->
    <div class="p-2.5 bg-slate-50 rounded-xl border border-slate-200 text-slate-700">
      <strong class="text-slate-800 block text-[11px] uppercase tracking-wide mb-1">Real English: Setting the Scene</strong>
      <p>The past progressive is often used to describe a scene in the past: <em>The café was full. A band was playing, and people were talking loudly. Everyone was enjoying the evening.</em></p>
      <p class="text-[11px] text-slate-500 pt-1 border-t border-slate-200 italic mt-1">See page A1 for spelling rules for the -ing form of verbs.</p>
    </div>
  </div>
</div>"""

CHART_2_4_HTML = """<div class="lg:col-span-5 bg-white rounded-2xl border border-slate-200 p-5 reader-card space-y-3">
  <div class="flex items-center justify-between border-b border-slate-100 pb-2">
    <h4 class="font-bold text-slate-900 text-sm sm:text-base">2.4 Past Progressive: Questions and Answers</h4>
    <span class="text-xs bg-slate-100 text-slate-600 px-2 py-0.5 rounded font-mono">Page 36</span>
  </div>

  <div class="space-y-3 text-xs">
    <!-- Yes/No Questions Table -->
    <div class="border border-slate-200 rounded-xl overflow-hidden shadow-sm">
      <div class="bg-slate-100 px-3 py-1.5 font-bold text-slate-700 flex items-center justify-between">
        <span>Yes / No Questions</span>
        <span class="text-[10px] text-slate-500 font-normal">Short Answers</span>
      </div>
      <div class="p-2.5 bg-white space-y-2 text-slate-700">
        <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-1 border-b border-slate-100 pb-1.5">
          <span><strong>Was</strong> I / he / she / it <strong>listening</strong> to music?</span>
          <span class="text-slate-600 font-medium">→ <em>Yes, she was. / No, she wasn’t.</em></span>
        </div>
        <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-1">
          <span><strong>Were</strong> you / we / they <strong>eating</strong> dinner?</span>
          <span class="text-slate-600 font-medium">→ <em>Yes, they were. / No, they weren’t.</em></span>
        </div>
      </div>
    </div>

    <!-- Wh- Questions Table -->
    <div class="border border-slate-200 rounded-xl overflow-hidden shadow-sm">
      <div class="bg-slate-100 px-3 py-1.5 font-bold text-slate-700 flex items-center justify-between">
        <span>Wh- Questions (Information)</span>
        <span class="text-[10px] text-slate-500 font-normal">Wh- + Was/Were + S + Verb-ing</span>
      </div>
      <div class="p-2.5 bg-white space-y-1.5 text-slate-700">
        <p>• <strong>What was</strong> he doing at 3:00? → <em class="text-slate-900 font-medium">He was working.</em></p>
        <p>• <strong>Where were</strong> you studying last night? → <em class="text-slate-900 font-medium">At the library.</em></p>
      </div>
    </div>

    <!-- Who or What as Subject -->
    <div class="border border-amber-200 rounded-xl overflow-hidden bg-amber-50/60 shadow-sm">
      <div class="bg-amber-100/80 px-3 py-1.5 font-bold text-amber-900 flex items-center justify-between">
        <span>Who or What as Subject</span>
        <span class="text-[10px] text-amber-800 font-normal">Who/What + Was + Verb-ing</span>
      </div>
      <div class="p-2.5 space-y-1.5 text-slate-800">
        <div class="flex items-center justify-between">
          <span>• <strong>Who was singing</strong> last night?</span>
          <span class="text-slate-600 font-medium">→ <em>Rita. / Alex and Rui.</em></span>
        </div>
        <div class="flex items-center justify-between">
          <span>• <strong>What was making</strong> that noise?</span>
          <span class="text-slate-600 font-medium">→ <em>My car.</em></span>
        </div>
        <div class="mt-2 pt-2 border-t border-amber-200 text-amber-900 text-[11px] leading-relaxed">
          <p><strong>Remember:</strong> <em>Who</em> or <em>What</em> can take the place of the subject in a Wh- question. When <em>Who</em> or <em>What</em> is the subject, the verb is singular (<em>was + verb-ing</em>):</p>
          <p class="font-medium mt-1">• A: <em>Who was playing that loud music last night?</em> → B: <em>Alex and Rui.</em></p>
        </div>
      </div>
    </div>
  </div>
</div>"""

CHART_2_5_HTML = """<div class="lg:col-span-5 bg-white rounded-2xl border border-slate-200 p-5 reader-card space-y-3">
  <div class="flex items-center justify-between border-b border-slate-100 pb-2">
    <h4 class="font-bold text-slate-900 text-sm sm:text-base">2.5 Past Time Clauses with When &amp; While</h4>
    <span class="text-xs bg-slate-100 text-slate-600 px-2 py-0.5 rounded font-mono">Page 41</span>
  </div>

  <div class="space-y-2.5 text-xs text-slate-700">
    <!-- Structure Table -->
    <div class="border border-slate-200 rounded-xl overflow-hidden shadow-sm">
      <div class="bg-slate-100 px-3 py-1.5 font-bold text-slate-700 flex items-center justify-between">
        <span>Clause Patterns</span>
        <span class="text-[10px] text-slate-500 font-normal">Main Clause &amp; Time Clause</span>
      </div>
      <div class="p-2.5 bg-white space-y-2 text-slate-700">
        <div class="space-y-1 border-b border-slate-100 pb-2">
          <span class="font-bold text-slate-800 block text-[11px]">With When:</span>
          <p>• <em>The storm began</em> [Main] <em>when I was driving home.</em> [Time Clause]</p>
          <p>• <em>When I was driving home<strong>,</strong></em> [Time Clause] <em>the storm began.</em> [Main]</p>
          <p>• <em>I was sleeping</em> [Main] <em>when you texted me.</em> [Time Clause]</p>
        </div>
        <div class="space-y-1">
          <span class="font-bold text-slate-800 block text-[11px]">With While:</span>
          <p>• <em>The storm began</em> [Main] <em>while we were walking home.</em> [Time Clause]</p>
          <p>• <em>While we were walking home<strong>,</strong></em> [Time Clause] <em>the storm began.</em> [Main]</p>
          <p>• <em>You texted me</em> [Main] <em>while I was sleeping.</em> [Time Clause]</p>
        </div>
      </div>
    </div>

    <!-- Explanations & Rules -->
    <div class="bg-slate-50 p-3 rounded-xl border border-slate-200 space-y-2 leading-relaxed">
      <div>
        <p><strong>1. Main Clause:</strong> Can stand alone as a complete sentence (<em>Elena called last night while I was cooking dinner.</em>).</p>
      </div>
      <div class="pt-1.5 border-t border-slate-200">
        <p><strong>2. Past Time Clause:</strong> Tells when an action happened. Can come before or after main clause (<em>When it started to snow, I was walking home. / It started to snow while I was walking home.</em>).</p>
      </div>
      <div class="pt-1.5 border-t border-slate-200">
        <p><strong>3. While / When + Past Progressive:</strong> Shows an action was in progress when another action happened:</p>
        <p class="text-slate-600">• <em>I broke my leg</em> [2nd Action] <em>when I was skiing.</em> [Action in Progress]</p>
        <p class="text-slate-600">• <em>Iris called</em> [2nd Action] <em>while I was cooking dinner.</em> [Action in Progress]</p>
      </div>
      <div class="pt-1.5 border-t border-slate-200">
        <p><strong>4. When + Simple Past:</strong> Used for an action that happened at a specific point in time:</p>
        <p class="text-slate-600">• <em>I was painting the living room</em> [In Progress] <em>when I fell off the ladder.</em> [Point in Time]</p>
      </div>
      <div class="pt-1.5 border-t border-slate-200 bg-amber-50/60 -mx-3 -mb-3 p-2.5 rounded-b-xl border-amber-200 text-amber-950">
        <p><strong>5. Comma Rule:</strong> Use a comma when the time clause comes <strong>first</strong> in the sentence:</p>
        <p class="text-slate-700">• <em>When we were taking the exam<strong>,</strong> the lights went out.</em> (Comma)</p>
        <p class="text-slate-700">• <em>The lights went out when we were taking the exam.</em> (No comma)</p>
      </div>
    </div>
  </div>
</div>"""

CHART_2_6_HTML = """<div class="lg:col-span-5 bg-white rounded-2xl border border-slate-200 p-5 reader-card space-y-3">
  <div class="flex items-center justify-between border-b border-slate-100 pb-2">
    <h4 class="font-bold text-slate-900 text-sm sm:text-base">2.6 Events in Sequence: When</h4>
    <span class="text-xs bg-slate-100 text-slate-600 px-2 py-0.5 rounded font-mono">Page 42</span>
  </div>

  <div class="space-y-3 text-xs text-slate-700">
    <!-- Rule 1 -->
    <div class="p-3 bg-slate-50 rounded-xl border border-slate-200 space-y-1.5">
      <strong class="text-slate-800 block text-[11px] uppercase tracking-wide">1. Actions in Sequence (Simple Past in Both):</strong>
      <p>When two actions happened one after the other, use the <strong>simple past</strong> in both the time clause and the main clause. Use <strong>when</strong> to introduce the time clause:</p>
      <div class="p-2 bg-white rounded-lg border border-slate-200 text-slate-800 font-medium">
        <p>• <em>When her phone rang, she answered it.</em></p>
        <p class="text-[11px] text-teal-700 mt-0.5">➔ Time Clause: 1st Event (phone rang) | Main Clause: 2nd Event (she answered)</p>
      </div>
    </div>

    <!-- Rule 2 -->
    <div class="p-3 bg-slate-50 rounded-xl border border-slate-200 space-y-1.5">
      <strong class="text-slate-800 block text-[11px] uppercase tracking-wide">2. Clause Position &amp; Meaning:</strong>
      <p>The past time clause can come first or second in the sentence. The action in the past time clause always happened first:</p>
      <p>• <em>When I got home<strong>,</strong> I took a shower.</em> (1st: got home ➔ 2nd: took a shower)</p>
      <p>• <em>I took a shower when I got home.</em> (2nd: took a shower ➔ 1st: got home)</p>
    </div>

    <!-- Rule 3: Comma -->
    <div class="p-3 bg-amber-50/70 rounded-xl border border-amber-200 text-amber-950 space-y-1">
      <strong class="text-amber-900 block text-[11px] uppercase tracking-wide">3. Comma Rule:</strong>
      <p>Remember: Use a comma when the past time clause comes first in the sentence:</p>
      <p class="font-medium text-slate-800 mt-0.5">• <em>When Joe saw the accident<strong>,</strong> he called the police.</em></p>
    </div>
  </div>
</div>"""

CHART_2_7_HTML = """<div class="lg:col-span-5 bg-white rounded-2xl border border-slate-200 p-5 reader-card space-y-3">
  <div class="flex items-center justify-between border-b border-slate-100 pb-2">
    <h4 class="font-bold text-slate-900 text-sm sm:text-base">2.7 Used To: Affirmative &amp; Negative Statements</h4>
    <span class="text-xs bg-slate-100 text-slate-600 px-2 py-0.5 rounded font-mono">Page 47</span>
  </div>

  <div class="space-y-3 text-xs text-slate-700">
    <!-- Affirmative & Negative Form -->
    <div class="border border-slate-200 rounded-xl overflow-hidden shadow-sm">
      <div class="bg-slate-100 px-3 py-1.5 font-bold text-slate-700 flex items-center justify-between">
        <span>Used To Statements</span>
        <span class="text-[10px] text-slate-500 font-normal">Past Habit / State</span>
      </div>
      <div class="p-2.5 bg-white space-y-2 text-slate-700">
        <div>
          <span class="font-bold text-teal-800 block text-[11px]">Affirmative (Subject + used to + Base Form):</span>
          <p class="text-slate-800 font-medium mt-0.5">• I / She / They <strong>used to study</strong> history.</p>
        </div>
        <div class="pt-2 border-t border-slate-100">
          <span class="font-bold text-rose-800 block text-[11px]">Negative (Subject + didn’t use to + Base Form):</span>
          <p class="text-slate-800 font-medium mt-0.5">• I / She / They <strong>didn’t use to study</strong> math.</p>
        </div>
      </div>
    </div>

    <!-- Explanations & Meaning -->
    <div class="bg-slate-50 p-3 rounded-xl border border-slate-200 space-y-2 leading-relaxed">
      <div>
        <p><strong>1. Habit or State That No Longer Exists:</strong></p>
        <p class="text-slate-600">• <em>I used to run several times a week.</em> (Now, I don’t.)</p>
        <p class="text-slate-600">• <em>I used to live in a small town.</em> (I live in a city now.)</p>
        <p class="text-slate-600">• <em>I didn’t use to eat meat.</em> (I do now.)</p>
      </div>

      <div class="pt-2 border-t border-slate-200">
        <p><strong>2. Negative Spelling:</strong> In negative statements, write <strong>didn’t use to</strong> (NOT <em>used to</em>):</p>
        <p class="font-mono text-[11px] text-emerald-800">✓ I didn’t use to love math.</p>
        <p class="font-mono text-[11px] text-rose-600">✗ I didn’t used to love math.</p>
      </div>
    </div>

    <!-- Real English & Pronunciation -->
    <div class="bg-amber-50/70 p-3 rounded-xl border border-amber-200 text-amber-950 space-y-1.5">
      <span class="font-bold text-amber-900 block text-[11px] uppercase tracking-wide">Real English</span>
      <p>Use <em>used to</em> instead of the simple past to emphasize that the habit or state is <strong>not true now</strong>:</p>
      <p class="italic text-slate-800">• When I was young, I used to go to the beach every day.</p>
      <p class="text-[11px] text-slate-600 pt-1 border-t border-amber-200/60">🗣️ <strong>Pronunciation:</strong> <em>used to</em> and <em>use to</em> are pronounced <strong>/ˈjuːstə/</strong>.</p>
    </div>
  </div>
</div>"""

CHART_2_8_HTML = """<div class="lg:col-span-5 bg-white rounded-2xl border border-slate-200 p-5 reader-card space-y-3">
  <div class="flex items-center justify-between border-b border-slate-100 pb-2">
    <h4 class="font-bold text-slate-900 text-sm sm:text-base">2.8 Used To: Questions and Answers</h4>
    <span class="text-xs bg-slate-100 text-slate-600 px-2 py-0.5 rounded font-mono">Page 48</span>
  </div>

  <div class="space-y-3 text-xs text-slate-700">
    <!-- Yes/No Questions Table -->
    <div class="border border-slate-200 rounded-xl overflow-hidden shadow-sm">
      <div class="bg-slate-100 px-3 py-1.5 font-bold text-slate-700 flex items-center justify-between">
        <span>Yes / No Questions</span>
        <span class="text-[10px] text-slate-500 font-normal">Short Answers</span>
      </div>
      <div class="p-2.5 bg-white space-y-2 text-slate-700">
        <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-1 border-b border-slate-100 pb-1.5">
          <span><strong>Did</strong> he <strong>use to get</strong> good grades?</span>
          <span class="text-slate-600 font-medium">→ <em>Yes, he did. / No, he didn’t.</em></span>
        </div>
        <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-1">
          <span><strong>Did</strong> they <strong>use to get</strong> good grades?</span>
          <span class="text-slate-600 font-medium">→ <em>Yes, they did. / No, they didn’t.</em></span>
        </div>
      </div>
    </div>

    <!-- Wh- Questions Table -->
    <div class="border border-slate-200 rounded-xl overflow-hidden shadow-sm">
      <div class="bg-slate-100 px-3 py-1.5 font-bold text-slate-700 flex items-center justify-between">
        <span>Wh- Questions (Information)</span>
        <span class="text-[10px] text-slate-500 font-normal">Wh- + Did + S + Use To + Base</span>
      </div>
      <div class="p-2.5 bg-white space-y-1.5 text-slate-700">
        <p>• <strong>Where did</strong> she <strong>use to live</strong>? → <em class="text-slate-900 font-medium">In Mexico.</em></p>
        <p>• <strong>Who did</strong> you <strong>use to study</strong> with? → <em class="text-slate-900 font-medium">My friend, Felix.</em></p>
      </div>
    </div>

    <!-- Who or What as Subject -->
    <div class="border border-purple-200 rounded-xl overflow-hidden bg-purple-50/60 shadow-sm">
      <div class="bg-purple-100/80 px-3 py-1.5 font-bold text-purple-900 flex items-center justify-between">
        <span>Who or What as Subject</span>
        <span class="text-[10px] text-purple-800 font-normal">Who/What + Used To + Base</span>
      </div>
      <div class="p-2.5 space-y-1.5 text-slate-800">
        <div class="flex items-center justify-between">
          <span>• <strong>Who used to teach</strong> this class?</span>
          <span class="text-slate-600 font-medium">→ <em>Professor Ortiz.</em></span>
        </div>
        <div class="flex items-center justify-between">
          <span>• <strong>What used to be</strong> here?</span>
          <span class="text-slate-600 font-medium">→ <em>A shoe store.</em></span>
        </div>
        <div class="mt-2 pt-2 border-t border-purple-200 text-purple-950 text-[11px] leading-relaxed">
          <p>⚠️ <strong>Be careful!</strong> When Who or What is the subject, use <strong>used to</strong> (NOT <em>use to</em>, and do NOT use <em>did</em>!):</p>
          <p class="font-mono text-[11px] text-emerald-800 mt-0.5">✓ Who used to live in that house?</p>
          <p class="font-mono text-[11px] text-rose-600">✗ Who use to live in that house? / ✗ Who did use to live in that house?</p>
        </div>
      </div>
    </div>

    <!-- General Question Rule -->
    <div class="p-2.5 bg-slate-50 rounded-xl border border-slate-200 text-slate-700">
      <p><strong>Rule with Did:</strong> When a question includes <em>did</em>, write <strong>use to</strong>, not <em>used to</em> (<em>Did you use to live here? / Where did she use to work?</em>).</p>
    </div>
  </div>
</div>"""

CHART_2_9_HTML = """<div class="lg:col-span-5 bg-white rounded-2xl border border-slate-200 p-5 reader-card space-y-3">
  <div class="flex items-center justify-between border-b border-slate-100 pb-2">
    <h4 class="font-bold text-slate-900 text-sm sm:text-base">2.9 Would: Repeated Past Actions</h4>
    <span class="text-xs bg-slate-100 text-slate-600 px-2 py-0.5 rounded font-mono">Page 50</span>
  </div>

  <div class="space-y-3 text-xs text-slate-700">
    <!-- Affirmative & Negative Form Table -->
    <div class="border border-slate-200 rounded-xl overflow-hidden shadow-sm">
      <div class="bg-slate-100 px-3 py-1.5 font-bold text-slate-700 flex items-center justify-between">
        <span>Would Statements</span>
        <span class="text-[10px] text-slate-500 font-normal">Would + Base Form</span>
      </div>
      <div class="p-2.5 bg-white space-y-2 text-slate-700">
        <div>
          <span class="font-bold text-teal-800 block text-[11px]">Affirmative (would / 'd):</span>
          <p class="text-slate-800 font-medium mt-0.5">• When I was in high school, I <strong>would (’d) ride</strong> my bike to school.</p>
        </div>
        <div class="pt-2 border-t border-slate-100">
          <span class="font-bold text-rose-800 block text-[11px]">Negative (would not / wouldn't):</span>
          <p class="text-slate-800 font-medium mt-0.5">• When Scott was a child, he <strong>would not (wouldn’t) eat</strong> any vegetables.</p>
        </div>
      </div>
    </div>

    <!-- Usage Note -->
    <div class="bg-slate-50 p-3 rounded-xl border border-slate-200 space-y-1.5 leading-relaxed">
      <strong class="text-slate-800 block text-[11px] uppercase tracking-wide">Repeated Past Actions:</strong>
      <p><em>Would</em> expresses a repeated past action or habit that no longer exists:</p>
      <p class="text-slate-600">• <em>In high school, we would play soccer every afternoon.</em></p>
      <p class="text-slate-600">• <em>As a child, I wouldn’t study, but I would get good grades.</em></p>
    </div>

    <!-- Critical Distinction: Actions vs States -->
    <div class="border border-rose-200 rounded-xl p-3 bg-rose-50/80 text-rose-950 space-y-1.5 shadow-sm">
      <div class="flex items-center gap-1.5 font-bold text-rose-900">
        <svg class="w-4 h-4 text-rose-600 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/></svg>
        <span>Be Careful! Actions vs. Past States</span>
      </div>
      <p>Do <strong>not</strong> use <em>would</em> for past situations or states that no longer exist. Use <strong>used to</strong> or <strong>didn’t use to</strong> instead!</p>
      <div class="space-y-1 pt-1 font-mono text-[11px]">
        <p class="text-emerald-800">✓ There used to be a library on this street. <span class="text-slate-500 font-sans italic">(state)</span></p>
        <p class="text-rose-600">✗ There would be a library on this street.</p>
        <p class="text-emerald-800">✓ He didn’t use to live on Palm Street. <span class="text-slate-500 font-sans italic">(state)</span></p>
        <p class="text-rose-600">✗ He wouldn’t live on Palm Street.</p>
      </div>
    </div>
  </div>
</div>"""

GRAMMAR_FOCUS_HTML = """<div class="bg-teal-50 rounded-xl border border-teal-200 p-4 text-xs text-teal-950 space-y-1.5">
  <span class="font-bold text-teal-900 block text-xs uppercase tracking-wide">GRAMMAR FOCUS: Simple Past, Past Progressive &amp; Time Clauses (Page 56)</span>
  <p class="text-slate-700">In the narrative story, the writer uses three key grammar structures to tell about a difficult experience:</p>
  <div class="space-y-1.5 text-slate-800 font-medium pl-2 border-l-2 border-teal-500 mt-1">
    <p>• <strong>Simple Past for completed actions &amp; events:</strong><br><span class="text-slate-600 italic">I looked out my window. My parents came and got me.</span></p>
    <p>• <strong>Past Progressive to describe a scene in the past:</strong><br><span class="text-slate-600 italic">The river was rising very quickly.</span></p>
    <p>• <strong>Past Time Clauses to describe when actions happened:</strong><br><span class="text-slate-600 italic">When I was a young girl, we lived near a river.</span></p>
  </div>
</div>"""

def find_chart_card(soup, prefix):
    for c in soup.select('.reader-card'):
        h = c.find(['h2', 'h3', 'h4', 'h5'])
        if h and prefix in h.get_text():
            return c
    return None

def update_u2_all_in_one():
    fpath = 'Grammar-Explorer-book/Grammar-Explorer-2/Unit 2/GE2 - U2.html'
    soup = BeautifulSoup(open(fpath, encoding='utf-8'), 'html.parser')
    
    # 2.1
    c21 = find_chart_card(soup, '2.1')
    if c21:
        new_tag = BeautifulSoup(CHART_2_1_HTML, 'html.parser').find(class_='reader-card')
        c21.replace_with(new_tag)
        print("  + Replaced Chart 2.1 in GE2 - U2.html")

    # 2.2
    c22 = find_chart_card(soup, '2.2')
    if c22:
        new_tag = BeautifulSoup(CHART_2_2_HTML, 'html.parser').find(class_='reader-card')
        c22.replace_with(new_tag)
        print("  + Replaced Chart 2.2 in GE2 - U2.html")

    # 2.3
    c23 = find_chart_card(soup, '2.3')
    if c23:
        new_tag = BeautifulSoup(CHART_2_3_HTML, 'html.parser').find(class_='reader-card')
        c23.replace_with(new_tag)
        print("  + Replaced Chart 2.3 in GE2 - U2.html")

    # 2.4
    c24 = find_chart_card(soup, '2.4')
    if c24:
        new_tag = BeautifulSoup(CHART_2_4_HTML, 'html.parser').find(class_='reader-card')
        c24.replace_with(new_tag)
        print("  + Replaced Chart 2.4 in GE2 - U2.html")

    # 2.5
    c25 = find_chart_card(soup, '2.5')
    if c25:
        new_tag = BeautifulSoup(CHART_2_5_HTML, 'html.parser').find(class_='reader-card')
        c25.replace_with(new_tag)
        print("  + Replaced Chart 2.5 in GE2 - U2.html")

    # 2.6
    c26 = find_chart_card(soup, '2.6')
    if c26:
        new_tag = BeautifulSoup(CHART_2_6_HTML, 'html.parser').find(class_='reader-card')
        c26.replace_with(new_tag)
        print("  + Replaced Chart 2.6 in GE2 - U2.html")

    # 2.7
    c27 = find_chart_card(soup, '2.7')
    if c27:
        new_tag = BeautifulSoup(CHART_2_7_HTML, 'html.parser').find(class_='reader-card')
        c27.replace_with(new_tag)
        print("  + Replaced Chart 2.7 in GE2 - U2.html")

    # 2.8
    c28 = find_chart_card(soup, '2.8')
    if c28:
        new_tag = BeautifulSoup(CHART_2_8_HTML, 'html.parser').find(class_='reader-card')
        c28.replace_with(new_tag)
        print("  + Replaced Chart 2.8 in GE2 - U2.html")

    # 2.9: Fix grid container with Ex 7
    ex7 = soup.find(id='ex7-l4-card')
    if ex7:
        # Check grandparent or parent
        gp = ex7.parent.parent if ex7.parent and 'lg:col-span-7' in ex7.parent.get('class', []) else ex7.parent
        if gp and 'grid' in gp.get('class', []):
            # Check if there is an lg:col-span-5 child
            col5 = gp.find(class_=lambda x: x and 'lg:col-span-5' in x)
            new_c29 = BeautifulSoup(CHART_2_9_HTML, 'html.parser').find(class_='reader-card')
            if col5:
                # If col5 has the section header, extract section header before gp!
                sec_hdr = col5.find(text=re.compile('Repeated Actions with Would'))
                if sec_hdr:
                    hdr_card = sec_hdr.find_parent(class_=lambda x: x and 'reader-card' in x)
                    if hdr_card:
                        gp.insert_before(hdr_card)
                col5.replace_with(new_c29)
                print("  + Replaced col5 with Chart 2.9 in GE2 - U2.html")
            else:
                ex7.insert_before(new_c29)
                print("  + Inserted Chart 2.9 before Ex 7 in GE2 - U2.html")
        else:
            # ex7 might be directly in a grid
            c29_exist = find_chart_card(soup, '2.9')
            new_c29 = BeautifulSoup(CHART_2_9_HTML, 'html.parser').find(class_='reader-card')
            if c29_exist:
                c29_exist.replace_with(new_c29)
            else:
                ex7.insert_before(new_c29)
            print("  + Updated Chart 2.9 near Ex 7 in GE2 - U2.html")

    # Grammar Focus in Model Reading (tab-writing)
    for c in soup.select('#tab-writing .reader-card'):
        if 'Spring Flood' in c.get_text():
            if not c.find(text=re.compile('GRAMMAR FOCUS')):
                writing_focus = c.find(text=re.compile('WRITING FOCUS'))
                gf_tag = BeautifulSoup(GRAMMAR_FOCUS_HTML, 'html.parser')
                if writing_focus:
                    wf_box = writing_focus.find_parent(class_=lambda x: x and 'rounded-xl' in x)
                    if wf_box:
                        wf_box.insert_before(gf_tag)
                    else:
                        c.append(gf_tag)
                else:
                    c.append(gf_tag)
                print("  + Added GRAMMAR FOCUS to Model Reading in GE2 - U2.html")
            break

    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(str(soup))
    print("[SUCCESS] GE2 - U2.html updated!")

def update_u2_lesson_1():
    fpath = 'Grammar-Explorer-book/Grammar-Explorer-2/Unit 2/grammar_explorer_2_unit_2_lesson_1.html'
    soup = BeautifulSoup(open(fpath, encoding='utf-8'), 'html.parser')

    c21 = find_chart_card(soup, '2.1')
    if c21:
        new_tag = BeautifulSoup(CHART_2_1_HTML, 'html.parser').find(class_='reader-card')
        c21.replace_with(new_tag)
        print("  + Replaced Chart 2.1 in grammar_explorer_2_unit_2_lesson_1.html")

    c22 = find_chart_card(soup, '2.2')
    if c22:
        new_tag = BeautifulSoup(CHART_2_2_HTML, 'html.parser').find(class_='reader-card')
        c22.replace_with(new_tag)
        print("  + Replaced Chart 2.2 in grammar_explorer_2_unit_2_lesson_1.html")

    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(str(soup))
    print("[SUCCESS] grammar_explorer_2_unit_2_lesson_1.html updated!")

def update_u2_lesson_2():
    fpath = 'Grammar-Explorer-book/Grammar-Explorer-2/Unit 2/grammar_explorer_2_unit_2_lesson_2.html'
    soup = BeautifulSoup(open(fpath, encoding='utf-8'), 'html.parser')

    c23 = find_chart_card(soup, '2.3')
    if c23:
        new_tag = BeautifulSoup(CHART_2_3_HTML, 'html.parser').find(class_='reader-card')
        c23.replace_with(new_tag)
        print("  + Replaced Chart 2.3 in grammar_explorer_2_unit_2_lesson_2.html")

    c24 = find_chart_card(soup, '2.4')
    if c24:
        new_tag = BeautifulSoup(CHART_2_4_HTML, 'html.parser').find(class_='reader-card')
        c24.replace_with(new_tag)
        print("  + Replaced Chart 2.4 in grammar_explorer_2_unit_2_lesson_2.html")

    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(str(soup))
    print("[SUCCESS] grammar_explorer_2_unit_2_lesson_2.html updated!")

def update_u2_lesson_3():
    fpath = 'Grammar-Explorer-book/Grammar-Explorer-2/Unit 2/grammar_explorer_2_unit_2_lesson_3.html'
    soup = BeautifulSoup(open(fpath, encoding='utf-8'), 'html.parser')

    c25 = find_chart_card(soup, '2.5')
    if c25:
        new_tag = BeautifulSoup(CHART_2_5_HTML, 'html.parser').find(class_='reader-card')
        c25.replace_with(new_tag)
        print("  + Replaced Chart 2.5 in grammar_explorer_2_unit_2_lesson_3.html")

    c26 = find_chart_card(soup, '2.6')
    if c26:
        new_tag = BeautifulSoup(CHART_2_6_HTML, 'html.parser').find(class_='reader-card')
        c26.replace_with(new_tag)
        print("  + Replaced Chart 2.6 in grammar_explorer_2_unit_2_lesson_3.html")

    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(str(soup))
    print("[SUCCESS] grammar_explorer_2_unit_2_lesson_3.html updated!")

def update_u2_lesson_4():
    fpath = 'Grammar-Explorer-book/Grammar-Explorer-2/Unit 2/grammar_explorer_2_unit_2_lesson_4.html'
    soup = BeautifulSoup(open(fpath, encoding='utf-8'), 'html.parser')

    c27 = find_chart_card(soup, '2.7')
    if c27:
        new_tag = BeautifulSoup(CHART_2_7_HTML, 'html.parser').find(class_='reader-card')
        c27.replace_with(new_tag)
        print("  + Replaced Chart 2.7 in grammar_explorer_2_unit_2_lesson_4.html")

    c28 = find_chart_card(soup, '2.8')
    if c28:
        new_tag = BeautifulSoup(CHART_2_8_HTML, 'html.parser').find(class_='reader-card')
        c28.replace_with(new_tag)
        print("  + Replaced Chart 2.8 in grammar_explorer_2_unit_2_lesson_4.html")

    c29 = find_chart_card(soup, '2.9')
    if c29:
        new_tag = BeautifulSoup(CHART_2_9_HTML, 'html.parser').find(class_='reader-card')
        c29.replace_with(new_tag)
        print("  + Replaced Chart 2.9 in grammar_explorer_2_unit_2_lesson_4.html")

    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(str(soup))
    print("[SUCCESS] grammar_explorer_2_unit_2_lesson_4.html updated!")

def update_u2_review_writing():
    fpath = 'Grammar-Explorer-book/Grammar-Explorer-2/Unit 2/grammar_explorer_2_unit_2_review_writing.html'
    soup = BeautifulSoup(open(fpath, encoding='utf-8'), 'html.parser')

    for c in soup.select('.reader-card'):
        if 'Spring Flood' in c.get_text():
            if not c.find(text=re.compile('GRAMMAR FOCUS')):
                writing_focus = c.find(text=re.compile('WRITING FOCUS'))
                gf_tag = BeautifulSoup(GRAMMAR_FOCUS_HTML, 'html.parser')
                if writing_focus:
                    wf_box = writing_focus.find_parent(class_=lambda x: x and 'rounded-xl' in x)
                    if wf_box:
                        wf_box.insert_before(gf_tag)
                    else:
                        c.append(gf_tag)
                else:
                    c.append(gf_tag)
                print("  + Added GRAMMAR FOCUS to Model Reading in grammar_explorer_2_unit_2_review_writing.html")
            break

    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(str(soup))
    print("[SUCCESS] grammar_explorer_2_unit_2_review_writing.html updated!")

if __name__ == '__main__':
    print("Executing Unit 2 Grammar Content Updates...")
    update_u2_all_in_one()
    update_u2_lesson_1()
    update_u2_lesson_2()
    update_u2_lesson_3()
    update_u2_lesson_4()
    update_u2_review_writing()
    print("All Unit 2 grammar updates completed!")
