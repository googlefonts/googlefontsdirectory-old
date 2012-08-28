package com.google.lint.common;

import com.google.common.collect.Lists;
import com.google.common.collect.Maps;

import java.util.List;
import java.util.Map;

/**
 * @author tocman@gmail.com (Jeremie Lenfant-Engelmann)
 */
public class Context {

  private final Map<Severity, List<String>> reports = Maps.newHashMap(); 

  public void report(Severity severity, String report) {
    List<String> severityReports = reports.get(severity);
    if (severityReports == null) {
      severityReports = Lists.newArrayList();
      reports.put(severity, severityReports);
    }
    severityReports.add(report);
  }

  public void printReports() {
    for (Map.Entry<Severity, List<String>> entry : reports.entrySet()) {
      Severity severity = entry.getKey();
      for (String report : entry.getValue()) {
        System.out.println(String.format("[%s] %s", severity, report));
      }
    }
  }
}
